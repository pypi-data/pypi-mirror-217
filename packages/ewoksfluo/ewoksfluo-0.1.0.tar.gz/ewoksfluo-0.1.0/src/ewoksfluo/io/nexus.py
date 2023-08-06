import os
import logging
from contextlib import ExitStack
from typing import Mapping, Optional, Iterator

import h5py
from silx.io.h5py_utils import File
from ewoksdata.data.hdf5.dataset_writer import DatasetWriter

from .types import ScanData


logger = logging.getLogger(__name__)


def save_as_bliss_scan(
    filename: str,
    entry_name: str,
    scan_data: Iterator[ScanData],
    positioners: Optional[Mapping[str, float]] = None,
    title: Optional[str] = None,
    **openoptions
):
    openoptions.setdefault("mode", "a")
    os.makedirs(os.path.abspath(os.path.dirname(filename)), exist_ok=True)
    with File(filename, **openoptions) as f:
        if entry_name in f:
            logger.warning("%s::/%s already exists", filename, entry_name)
            return
        f.attrs["NX_class"] = "NXroot"
        f.attrs["creator"] = "ewoksfluo"
        entry = f.create_group(entry_name)
        entry.attrs["NX_class"] = "NXentry"
        instrument = entry.create_group("instrument")
        instrument.attrs["NX_class"] = "NXinstrument"
        measurement = entry.create_group("measurement")
        measurement.attrs["NX_class"] = "NXcollection"

        if title:
            entry["title"] = title

        if positioners:
            collection = instrument.create_group("positioners_start")
            collection.attrs["NX_class"] = "NXcollection"
            for k, v in positioners.items():
                collection[k] = v
            positioners = dict(positioners)

        with ExitStack() as stack:
            writers = dict()
            for data in scan_data:
                detector = instrument.require_group(data.group)
                if data.detector_type == "positioner":
                    detector.attrs["NX_class"] = "NXpositioner"
                    if positioners:
                        positioners[data.group] = data.data
                else:
                    detector.attrs["NX_class"] = "NXdetector"
                    if "type" not in detector and data.detector_type:
                        detector["type"] = data.detector_type

                key = data.group, data.name
                writer = writers.get(key)
                if writer is None:
                    writer = stack.enter_context(DatasetWriter(detector, data.name))
                    writers[key] = writer
                    if data.local_alias:
                        detector[data.local_alias] = h5py.SoftLink(writer.dataset_name)
                    if data.global_alias and data.global_alias not in measurement:
                        measurement[data.global_alias] = h5py.SoftLink(
                            writer.dataset_name
                        )

                writer.add_points(data.data)

        if positioners:
            collection = instrument.create_group("positioners")
            collection.attrs["NX_class"] = "NXcollection"
            for k, v in positioners.items():
                collection[k] = v
