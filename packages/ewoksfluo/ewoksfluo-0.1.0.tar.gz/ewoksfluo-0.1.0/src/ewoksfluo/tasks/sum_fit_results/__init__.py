from typing import Sequence

from ewokscore import Task

from .. import nexus as nx
from ..utils import save_in_ewoks_process
from .utils import compute_summed_fractions, compute_summed_parameters, save_summed_dict


class SumFitResults(
    Task,
    input_names=[
        "fit_results_uri_template",
        "scan_uri",
        "livetime_uri_template",
        "detector_names",
        "livetime_reference_value",
        "output_uri",
    ],
    output_names=["summed_results_uri"],
):
    def run(self) -> None:
        start_time = nx.now()
        fit_results_uri_template: str = self.inputs.fit_results_uri_template
        scan_uri: str = self.inputs.scan_uri
        livetime_uri_template: str = self.inputs.livetime_uri_template
        detector_names: Sequence[str] = self.inputs.detector_names
        livetime_reference_value: float = self.inputs.livetime_reference_value
        output_uri: str = self.inputs.output_uri

        fit_results_uris = [
            fit_results_uri_template.format(detector_name=d) for d in detector_names
        ]
        livetime_uris = [
            f"{scan_uri}/{livetime_uri_template.format(detector_name=d)}"
            for d in detector_names
        ]

        (
            summed_parameters,
            summed_uncertainties,
            has_massfractions,
        ) = compute_summed_parameters(
            fit_results_uris, livetime_uris, livetime_reference_value
        )

        if has_massfractions:
            summed_fractions = compute_summed_fractions(
                fit_results_uris,
                livetime_uris,
                livetime_reference_value,
                summed_parameters,
            )
        else:
            summed_fractions = None

        with save_in_ewoks_process(
            output_uri,
            start_time,
            process_config={"livetime_reference_value": livetime_reference_value},
        ) as process_group:
            results_group = process_group.create_group("results")
            results_group.attrs["NX_class"] = "NXcollection"

            param_group = save_summed_dict(
                results_group, "parameters", summed_parameters
            )
            error_group = save_summed_dict(
                results_group, "uncertainties", summed_uncertainties
            )
            # Add `errors` links
            for name in param_group:
                param_group[f"{name}_errors"] = error_group[name]

            if summed_fractions is not None:
                save_summed_dict(results_group, "massfractions", summed_fractions)

        self.outputs.summed_results_uri = f"{output_uri}/results"
