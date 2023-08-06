from typing import Sequence

import numpy
import h5py
from ewokscore import Task

from .. import nexus
from ..utils import (
    get_correction_factor,
    save_in_ewoks_process,
)


class SumDetectors(
    Task,
    input_names=[
        "scan_uri",
        "detector_names",
        "xrf_spectra_uri_template",
        "livetime_uri_template",
        "livetime_reference_value",
        "output_uri",
    ],
    output_names=[
        "scan_uri",
        "detector_name",
        "xrf_spectra_uri_template",
    ],
):
    def run(self):
        start_time = nexus.now()
        scan_uri: str = self.inputs.scan_uri
        detector_names: Sequence[str] = self.inputs.detector_names
        xrf_spectra_uri_template: str = self.inputs.xrf_spectra_uri_template
        livetime_uri_template: str = self.inputs.livetime_uri_template
        output_uri: str = self.inputs.output_uri
        livetime_ref_value: float = self.inputs.livetime_reference_value

        if len(detector_names) < 1:
            raise ValueError("Expected at least 1 detector to sum")

        input_file, scan_h5path = scan_uri.split("::")

        with h5py.File(input_file, "r") as h5file:
            summed_data = None
            scan_group = h5file[scan_h5path]

            for detector_name in detector_names:
                xrf_spectra_dataset = scan_group[
                    xrf_spectra_uri_template.format(detector_name=detector_name)
                ]
                assert isinstance(xrf_spectra_dataset, h5py.Dataset)
                xrf_spectra_data = xrf_spectra_dataset[()]

                livetime_uri = f"{scan_uri}/{livetime_uri_template.format(detector_name=detector_name)}"
                correction = get_correction_factor([livetime_uri], [livetime_ref_value])

                if summed_data is None:
                    summed_data = numpy.zeros_like(
                        xrf_spectra_data, dtype="float32"
                    )  # Cast to float since the correction is a floating-point division

                summed_data += xrf_spectra_data * correction.reshape(
                    (len(correction), 1)
                )

        with save_in_ewoks_process(
            output_uri,
            start_time,
            process_config={"livetime_reference_value": livetime_ref_value},
        ) as process_group:
            results_group = nexus.create_data(process_group, "results", signal="data")
            results_group.create_dataset("data", data=summed_data)

        self.outputs.scan_uri = output_uri
        self.outputs.detector_name = "results"
        self.outputs.xrf_spectra_uri_template = "{detector_name}/data"
