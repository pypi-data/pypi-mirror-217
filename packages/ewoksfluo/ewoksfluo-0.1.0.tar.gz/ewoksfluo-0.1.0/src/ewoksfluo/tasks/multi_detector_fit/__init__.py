from queue import Queue
from typing import Dict, Optional, Sequence, Set, Tuple, Union
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


class MultiDetectorFit(
    Task,
    input_names=[
        "scan_uri",
        "detector_names",
        "xrf_spectra_uri_template",
        "configs",
        "output_uri_template",
    ],
    optional_input_names=[
        "energy",
        "quantification",
        "energy_multiplier",
        "fast_fitting",
        "diagnostics",
        "figuresofmerit",
    ],
    output_names=["fit_results_uri_template", "detector_names"],
):
    def run(self):
        scan_uri: str = self.inputs.scan_uri
        detector_names: Sequence[str] = self.inputs.detector_names
        xrf_spectra_uri_template: str = self.inputs.xrf_spectra_uri_template
        configs: Sequence[Union[str, ConfigDict]] = self.inputs.configs
        output_uri_template: str = self.inputs.output_uri_template
        energy: Optional[float] = self.get_input_value("energy", None)
        quantification: Optional[dict] = self.get_input_value("quantification", None)
        energy_multiplier: float = self.get_input_value("energy_multiplier", 0)
        fast_fitting: bool = self.get_input_value("fast_fitting", True)
        diagnostics: bool = self.get_input_value("diagnostics", False)
        figuresofmerit: bool = self.get_input_value("figuresofmerit", False)

        output_handlers: Dict[int, NexusOutputHandler] = dict()
        queue_sendids: Set[int] = set()

        with ExitStack() as stack:
            ctx = multiprocessing.Manager()
            manager = stack.enter_context(ctx)
            queue = manager.Queue()

            ctx = ProcessPoolExecutor()
            executor = stack.enter_context(ctx)

            arguments = list()
            queue_sendid = 0
            for detector_name, config in zip(detector_names, configs):
                output_uri = output_uri_template.format(detector_name=detector_name)
                ctx = NexusOutputHandler(output_uri)
                output_handler = stack.enter_context(ctx)
                if output_handler.already_existed:
                    print(f"Already saved in {output_handler.fit_results_uri}")
                    continue

                queue_sendids.add(queue_sendid)
                destinationid = queue_sendid
                output_handlers[destinationid] = output_handler

                buffer_args = queue, queue_sendid, destinationid
                buffer_kwargs = {
                    "diagnostics": diagnostics,
                    "figuresofmerit": figuresofmerit,
                }
                fit_kwargs = {
                    "xrf_spectra_uris": [
                        f"{scan_uri}/{xrf_spectra_uri_template.format(detector_name=detector_name)}"
                    ],
                    "cfg": config,
                    "energy": energy,
                    "energy_multiplier": energy_multiplier,
                    "quantification": quantification,
                    "fast": fast_fitting,
                }
                arguments.append((buffer_args, buffer_kwargs, fit_kwargs))
                queue_sendid += 1

            # Sub-processes will fit send the results to the queue
            arguments = list(zip(*arguments))
            results = executor.map(_fit_main, *arguments, chunksize=1)

            # Main process will receive results from the queue and save them in HDF5
            consume_handler_queue(output_handlers, queue, queue_sendids)

            # Re-raise exceptions if any
            for result in results:
                pass

        self.outputs.fit_results_uri_template = f"{output_uri_template}/results"
        self.outputs.detector_names = detector_names


def _fit_main(
    buffer_args: Tuple[Queue, int],
    buffer_kwargs: dict,
    fit_kwargs: dict,
) -> None:
    queue, sendid, destinationid = buffer_args
    try:
        with queue_outputbuffer_context(
            queue, sendid, destinationid, **buffer_kwargs
        ) as output_buffer:
            perform_batch_fit(output_buffer=output_buffer, **fit_kwargs)
    finally:
        stop_queue(queue, sendid)
