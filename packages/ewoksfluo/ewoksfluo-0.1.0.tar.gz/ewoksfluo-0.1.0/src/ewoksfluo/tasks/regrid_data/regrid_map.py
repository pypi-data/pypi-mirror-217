from ewokscore import Task

import h5py

from ..utils import get_groups_to_correct, save_in_ewoks_collection

from .utils import (
    find_position_size,
    get_position_data,
    reshape_into_virtual_dset,
)
from .. import nexus as nx


class RegridOnCoordinates(
    Task,
    input_names=[
        "scan_uri",
        "fit_results_uri",
        "output_uri",
        "position1_suburi",
        "position2_suburi",
    ],
    output_names=["regridded_uri"],
):
    def run(self):
        start_time = nx.now()
        scan_uri: str = self.inputs.scan_uri
        fit_results_uri: str = self.inputs.fit_results_uri
        output_uri: str = self.inputs.output_uri
        position1_suburi: str = self.inputs.position1_suburi
        position2_suburi: str = self.inputs.position2_suburi

        x1_size = find_position_size(scan_uri, position1_suburi)
        x2_size = find_position_size(scan_uri, position2_suburi)

        fit_results_filename, fit_results_h5path = fit_results_uri.split("::")

        with save_in_ewoks_collection(output_uri, start_time, {}) as regrid_results:
            with h5py.File(fit_results_filename, "r") as fit_results_file:
                fit_results_grp = fit_results_file[fit_results_h5path]
                assert isinstance(fit_results_grp, h5py.Group)

                group_to_regrid = get_groups_to_correct(fit_results_grp)
                regrid_results.attrs["default"] = tuple(group_to_regrid.keys())[0]

                for group_name in group_to_regrid:
                    input_grp = fit_results_grp[group_name]
                    assert isinstance(input_grp, h5py.Group)

                    output_grp = nx.create_data(regrid_results, group_name)

                    # Signals
                    input_datasets = {
                        dset_name: dset
                        for dset_name, dset in input_grp.items()
                        if isinstance(dset, h5py.Dataset)
                    }

                    for dset_name, dset in input_datasets.items():
                        reshape_into_virtual_dset(
                            dset,
                            output_grp,
                            dset_name,
                            destination_shape=(x1_size, x2_size),
                        )

                    nx.set_data_signals(
                        output_grp, signals=tuple(input_datasets.keys())
                    )

                    # Axes
                    output_grp.create_dataset(
                        "x1",
                        data=get_position_data(scan_uri, position1_suburi).reshape(
                            (x1_size, x2_size)
                        ),
                    )
                    output_grp.create_dataset(
                        "x2",
                        data=get_position_data(scan_uri, position2_suburi).reshape(
                            (x1_size, x2_size)
                        ),
                    )
                    output_grp.attrs["axes"] = ["x1", "x2"]
                    output_grp.attrs["x1_indices"] = [0, 1]
                    output_grp.attrs["x2_indices"] = [0, 1]

        self.outputs.regridded_uri = f"{output_uri}/results"
