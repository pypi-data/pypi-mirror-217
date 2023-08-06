from typing import List, Dict
from ewoksorange.bindings import ows_to_ewoks
from ewokscore import execute_graph

try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources


def test_single_scan_sum_multi_detectors_without_qt(tmpdir):
    from orangecontrib.ewoksfluo import tutorials

    with resources.path(tutorials, "single_scan_sum_multi_detectors.ows") as filename:
        assert_single_scan_sum_multi_detectors_without_qt(filename, tmpdir)


def test_single_scan_sum_multi_detectors_with_qt(ewoks_orange_canvas, tmpdir):
    from orangecontrib.ewoksfluo import tutorials

    with resources.path(tutorials, "single_scan_sum_multi_detectors.ows") as filename:
        assert_single_scan_sum_multi_detectors_with_qt(
            ewoks_orange_canvas, filename, tmpdir
        )


def assert_single_scan_sum_multi_detectors_without_qt(filename, tmpdir):
    """Execute workflow after converting it to an ewoks workflow"""
    graph = ows_to_ewoks(filename)
    outputs = execute_graph(
        graph, inputs=get_inputs(tmpdir), outputs=[{"all": True}], merge_outputs=False
    )
    expected = get_expected_outputs(tmpdir)
    label_to_id = {
        attrs["label"]: node_id for node_id, attrs in graph.graph.nodes.items()
    }
    expected = {label_to_id[k]: v for k, v in expected.items()}
    assert outputs == expected


def assert_single_scan_sum_multi_detectors_with_qt(
    ewoks_orange_canvas, filename, tmpdir
):
    """Execute workflow using the Qt widgets and signals"""
    ewoks_orange_canvas.load_graph(str(filename), inputs=get_inputs(tmpdir))
    ewoks_orange_canvas.start_workflow()
    ewoks_orange_canvas.wait_widgets(timeout=10)
    outputs = dict(ewoks_orange_canvas.iter_output_values())
    assert outputs == get_expected_outputs(tmpdir)


def get_inputs(tmpdir) -> List[dict]:
    return [
        {
            "label": "Example XRF scan",
            "name": "output_filename",
            "value": str(tmpdir / "input.h5"),
        },
        {
            "label": "Sum Detectors",
            "name": "output_uri",
            "value": str(tmpdir / "output.h5::/1.1/sum"),
        },
        {
            "label": "Single-Detector Fit",
            "name": "output_uri",
            "value": str(tmpdir / "output.h5::/1.1/fit"),
        },
        {
            "label": "Normalization",
            "name": "output_uri",
            "value": str(tmpdir / "output.h5::/1.1/normalize"),
        },
    ]


def get_expected_outputs(tmpdir) -> Dict[str, dict]:
    return {
        "Example XRF scan": {
            "I0_reference_values": [10000],
            "I0_uris": [str(tmpdir / "input.h5::/1.1/measurement/I0")],
            "config": str(tmpdir / "input.h5::/1.1/theory/configuration/data"),
            "configs": [
                str(tmpdir / "input.h5::/1.1/theory/configuration/data"),
                str(tmpdir / "input.h5::/1.1/theory/configuration/data"),
            ],
            "energy": 10.0,
            "energies": [10.0],
            "livetime_reference_value": 0.1,
            "livetime_uris": [
                str(tmpdir / "input.h5::/1.1/measurement/mca0_live_time"),
                str(tmpdir / "input.h5::/1.1/measurement/mca1_live_time"),
            ],
            "normalize_reference_values": [10000, 0.1],
            "normalize_uris": [
                str(tmpdir / "input.h5::/1.1/measurement/I0"),
                str(tmpdir / "input.h5::/1.1/measurement/mca0_live_time"),
            ],
            "xrf_spectra_uri": str(tmpdir / "input.h5::/1.1/measurement/mca0"),
            "xrf_spectra_uris": [
                str(tmpdir / "input.h5::/1.1/measurement/mca0"),
                str(tmpdir / "input.h5::/1.1/measurement/mca1"),
            ],
            "scan_uri": str(tmpdir / "input.h5::/1.1"),
            "scan_uris": [str(tmpdir / "input.h5::/1.1")],
            "detector_name": "mca0",
            "detector_names": ["mca0", "mca1"],
            "xrf_spectra_uri_template": "measurement/{detector_name}",
            "livetime_uri_template": "measurement/{detector_name}_live_time",
        },
        "Sum Detectors": {
            "scan_uri": str(tmpdir / "output.h5::/1.1/sum"),
            "detector_name": "results",
            "xrf_spectra_uri_template": "{detector_name}/data",
        },
        "Single-Detector Fit": {
            "fit_results_uri": str(tmpdir / "output.h5::/1.1/fit/results")
        },
        "Normalization": {
            "corr_data_uri": str(tmpdir / "output.h5::/1.1/normalize/results")
        },
    }
