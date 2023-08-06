from queue import Queue
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from concurrent.futures import ProcessPoolExecutor
from contextlib import ExitStack
import multiprocessing


from ewokscore import Task
from PyMca5.PyMcaIO.ConfigDict import ConfigDict


from ...xrffit import perform_batch_fit
from ...xrffit import queue_outputbuffer_context
from ...xrffit.handlers import NexusOutputHandler
from ...xrffit.handlers import consume_handler_queue
from ...xrffit.handlers import stop_queue


class MultiScanFit(
    Task,
    input_names=[
        "scan_uris",
        "detector_names",
        "xrf_spectra_uri_template",
        "configs",
        "output_uris",
    ],
    optional_input_names=[
        "energies",
        "quantification",
        "energy_multiplier",
        "fast_fitting",
        "diagnostics",
        "figuresofmerit",
    ],
    output_names=["fit_results_uris"],
):
    def run(self):
        scan_uris: Sequence[str] = self.inputs.scan_uris
        detector_names: Sequence[str] = self.inputs.detector_names
        xrf_spectra_uri_template: str = self.inputs.xrf_spectra_uri_template
        configs: Sequence[Union[str, ConfigDict]] = self.inputs.configs
        output_uris: Sequence[str] = self.inputs.output_uris
        energies: Optional[Sequence[Optional[float]]] = self.get_input_value(
            "energies", [None] * len(scan_uris)
        )
        quantification: Optional[dict] = self.get_input_value("quantification", None)
        energy_multiplier: float = self.get_input_value("energy_multiplier", 0)
        fast_fitting: bool = self.get_input_value("fast_fitting", True)
        diagnostics: bool = self.get_input_value("diagnostics", False)
        figuresofmerit: bool = self.get_input_value("figuresofmerit", False)

        fit_results_uris: List[str] = []
        output_handlers: Dict[int, NexusOutputHandler] = dict()
        queue_sendids: Set[int] = set()

        nscans = len(scan_uris)

        with ExitStack() as stack:
            ctx = multiprocessing.Manager()
            manager = stack.enter_context(ctx)
            queue = manager.Queue()

            ctx = ProcessPoolExecutor()
            executor = stack.enter_context(ctx)

            arguments = list()
            for destinationid, (detector, cfg) in enumerate(
                zip(detector_names, configs)
            ):
                ctx = NexusOutputHandler(output_uris[destinationid])
                output_handler = stack.enter_context(ctx)
                fit_results_uris.append(output_handler.fit_results_uri)
                if output_handler.already_existed:
                    print(f"Already saved in {output_handler.fit_results_uri}")
                    continue
                output_handlers[destinationid] = output_handler

                for i_scan, (scan_uri, energy) in enumerate(zip(scan_uris, energies)):
                    queue_sendid = destinationid * nscans + i_scan
                    queue_sendids.add(queue_sendid)

                    buffer_args = (
                        queue,
                        queue_sendid,
                        destinationid,
                        nscans,
                        i_scan,
                    )
                    buffer_kwargs = {
                        "diagnostics": diagnostics,
                        "figuresofmerit": figuresofmerit,
                    }
                    fit_kwargs = {
                        "xrf_spectra_uris": [
                            f"{scan_uri}/{xrf_spectra_uri_template.format(detector_name=detector)}"
                        ],
                        "cfg": cfg,
                        "energy": energy,
                        "energy_multiplier": energy_multiplier,
                        "quantification": quantification,
                        "fast": fast_fitting,
                    }
                    arguments.append((buffer_args, buffer_kwargs, fit_kwargs))

            # Sub-processes will fit send the results to the queue
            arguments = list(zip(*arguments))
            results = executor.map(_fit_main, *arguments, chunksize=1)

            # Main process will receive results from the queue and save them in HDF5
            consume_handler_queue(output_handlers, queue, queue_sendids)

            # Re-raise exceptions if any
            for result in results:
                pass

        self.outputs.fit_results_uris = fit_results_uris


def _fit_main(
    buffer_args: Tuple[Queue, int, int, Optional[int], int],
    buffer_kwargs: dict,
    fit_kwargs: dict,
) -> None:
    queue, sendid, destinationid, nscans, scan_index = buffer_args
    try:
        with queue_outputbuffer_context(
            queue, sendid, destinationid, nscans, scan_index, **buffer_kwargs
        ) as output_buffer:
            perform_batch_fit(output_buffer=output_buffer, **fit_kwargs)
    finally:
        stop_queue(queue, sendid)
