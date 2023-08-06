from typing import Union, Optional

from ewokscore import Task
from PyMca5.PyMcaIO.ConfigDict import ConfigDict

from ...xrffit import perform_batch_fit
from ...xrffit import outputbuffer_context


class SingleDetectorFit(
    Task,
    input_names=[
        "scan_uri",
        "detector_name",
        "xrf_spectra_uri_template",
        "config",
        "output_uri",
    ],
    optional_input_names=[
        "energy",
        "quantification",
        "energy_multiplier",
        "fast_fitting",
        "diagnostics",
        "figuresofmerit",
    ],
    output_names=["fit_results_uri"],
):
    def run(self):
        scan_uri: str = self.inputs.scan_uri
        detector_name: str = self.inputs.detector_name
        xrf_spectra_uri_template: str = self.inputs.xrf_spectra_uri_template
        config: Union[str, ConfigDict] = self.inputs.config
        output_uri: str = self.inputs.output_uri
        energy: Optional[float] = self.get_input_value("energy", None)
        quantification: Optional[dict] = self.get_input_value("quantification", None)
        energy_multiplier: float = self.get_input_value("energy_multiplier", 0.0)
        fast_fitting: bool = self.get_input_value("fast_fitting", True)
        diagnostics: bool = self.get_input_value("diagnostics", False)
        figuresofmerit: bool = self.get_input_value("figuresofmerit", False)

        with outputbuffer_context(
            output_uri,
            diagnostics=diagnostics,
            figuresofmerit=figuresofmerit,
        ) as output_buffer:
            if output_buffer.already_existed:
                print(f"Already saved in {output_buffer.fit_results_uri}")
            else:
                perform_batch_fit(
                    xrf_spectra_uris=[
                        f"{scan_uri}/{xrf_spectra_uri_template.format(detector_name=detector_name)}"
                    ],
                    cfg=config,
                    output_buffer=output_buffer,
                    energy=energy,
                    energy_multiplier=energy_multiplier,
                    quantification=quantification,
                    fast=fast_fitting,
                )
            self.outputs.fit_results_uri = output_buffer.fit_results_uri
