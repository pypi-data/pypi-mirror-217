import contextlib
from typing import Any, Dict, Optional, Sequence, Union
import h5py
import numpy
import json
import os.path

from . import nexus as nx
from ewoksfluo import __version__ as version


@contextlib.contextmanager
def entry_group_context(
    file: h5py.File, entry_name: str, default: Optional[str] = None
):
    entry_group = file.get(entry_name, None)
    if entry_group is None:
        entry_group = nx.create_entry(file, entry_name, default=default)
    assert isinstance(entry_group, h5py.Group)
    # Update default in case of an existing entry_group
    entry_group.attrs["default"] = default

    try:
        yield entry_group
    finally:
        if "end_time" in entry_group:
            entry_group["end_time"][()] = nx.now()
        else:
            entry_group["end_time"] = nx.now()


@contextlib.contextmanager
def process_group_context(
    entry_group: h5py.Group,
    process_name: str,
    config: Dict[str, Any],
    default: Optional[str] = None,
):
    process_group = nx.create_process(
        entry_group,
        process_name,
        default=default,
    )
    process_group["program"] = "ewoksfluo"
    process_group["version"] = version
    config_group = process_group.create_group("configuration")
    config_group.create_dataset("data", data=json.dumps(config, cls=PyFaiEncoder))
    config_group.create_dataset("date", data=nx.now())
    config_group.create_dataset("type", data="json")

    yield process_group


class PyFaiEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (numpy.generic, numpy.ndarray)):
            return obj.tolist()
        return super().default(obj)


def get_time_in_seconds(time_dset: h5py.Dataset) -> numpy.ndarray:
    unit = time_dset.attrs.get("units", "s")

    if unit == "ms":
        return time_dset[()] / 1000

    if unit == "s":
        return time_dset[()]

    raise ValueError(f"Unknown unit {unit} in {time_dset.name}")


def get_correction_factor(
    normalize_uris: Sequence[str], normalize_reference_values: Sequence[float]
) -> Union[float, numpy.ndarray]:
    """
    Get correction factor by resolving normalize_uris:

        reference_1 / normalize_1 * ... reference_N / normalize_N
    """
    if len(normalize_uris) != len(normalize_reference_values):
        raise ValueError(
            "Monitor and reference lists should have the same number of elements!"
        )

    correction_factor = 1.0
    for normalize_uri, reference in zip(normalize_uris, normalize_reference_values):
        normalize_file, normalize_h5path = normalize_uri.split("::")

        with h5py.File(normalize_file, "r") as h5file:
            normalize_dset = h5file[normalize_h5path]
            assert isinstance(normalize_dset, h5py.Dataset)
            correction_factor = correction_factor * reference / normalize_dset[()]

    return correction_factor


@contextlib.contextmanager
def save_in_ewoks_process(
    output_uri: str, start_time: str, process_config: Dict[str, Any]
):
    output_file, output_h5path = output_uri.split("::")

    with h5py.File(output_file, "a") as output:
        entry_name, process_name = os.path.split(output_h5path)
        with entry_group_context(
            output, entry_name, default=process_name
        ) as entry_group:
            if "start_time" not in entry_group:
                entry_group["start_time"] = start_time

            with process_group_context(
                entry_group,
                process_name,
                config=process_config,
                default="results",
            ) as process_group:
                yield process_group


@contextlib.contextmanager
def save_in_ewoks_collection(
    output_uri: str,
    start_time: str,
    process_config: Dict[str, Any],
    collection_name: str = "results",
):
    with save_in_ewoks_process(output_uri, start_time, process_config) as process:
        results = process.create_group(collection_name)
        results.attrs["NX_class"] = "NXcollection"
        yield results


GROUPS_TO_CORRECT = ["massfractions", "parameters", "uncertainties"]


def get_groups_to_correct(parent_nxdata: h5py.Group) -> Dict[str, h5py.Group]:
    group_to_corr = {
        k: v
        for k, v in parent_nxdata.items()
        if k in GROUPS_TO_CORRECT and isinstance(v, h5py.Group)
    }

    if len(group_to_corr) == 0:
        raise ValueError(
            f"No group to correct in {parent_nxdata.name}! Groups to correct must be one of the following: {GROUPS_TO_CORRECT}"
        )

    return group_to_corr
