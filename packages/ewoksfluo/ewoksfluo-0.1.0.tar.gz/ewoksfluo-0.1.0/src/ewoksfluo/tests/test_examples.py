import h5py
from ewoksorange.tests.utils import execute_task

from orangecontrib.ewoksfluo.example_xrf_scan import OWExampleXRFScan


def test_example_xrf_scan_task(tmpdir):
    _test_example_xrf_scan(tmpdir, OWExampleXRFScan.ewokstaskclass)


def test_example_xrf_scan_widget(tmpdir, qtapp):
    _test_example_xrf_scan(tmpdir, OWExampleXRFScan)


def _test_example_xrf_scan(tmpdir, task_cls):
    filename = str(tmpdir / "test.h5")
    inputs = {"output_filename": filename, "ndetectors": 2}
    execute_task(task_cls, inputs)

    with h5py.File(filename) as f:
        measurement = f["/1.1/measurement"]
        expected = {"I0"}
        for i in range(2):
            expected.update(
                {
                    f"mca{i}",
                    f"mca{i}_events",
                    f"mca{i}_triggers",
                    f"mca{i}_event_count_rate",
                    f"mca{i}_trigger_count_rate",
                    f"mca{i}_elapsed_time",
                    f"mca{i}_live_time",
                    f"mca{i}_trigger_live_time",
                    f"mca{i}_fractional_dead_time",
                }
            )
        assert set(measurement) == expected
        for k in measurement:
            assert measurement[k][()].ndim > 0
