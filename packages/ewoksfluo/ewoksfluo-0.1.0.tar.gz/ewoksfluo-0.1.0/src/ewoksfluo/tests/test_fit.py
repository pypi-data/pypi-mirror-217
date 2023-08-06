from typing import List, Iterator, Tuple, Dict

import numpy
import h5py
import pytest

from ewoksfluo.xrffit import perform_batch_fit
from ewoksfluo.xrffit import outputbuffer_context
from ewoksfluo.tests.data.xrf_spectra import EmissionLineGroup
from ewoksfluo.tests.data.xrf_spectra import ScatterLineGroup
from ewoksfluo.tests.data.xrf_spectra import xrf_spectra


@pytest.mark.parametrize("nscans", [1, 2])
@pytest.mark.parametrize("npoints_per_scan", [1, 7, 200])
@pytest.mark.parametrize("fast", [True, False])
@pytest.mark.parametrize("output_handler", ["nexus", "pymca"])
@pytest.mark.parametrize("samefile", [True, False])
def test_single_detector_fit(
    tmpdir, nscans, npoints_per_scan, fast, output_handler, samefile
):
    if not fast and npoints_per_scan > 10:
        pytest.skip("too slow, no extra value in testing")
    if not samefile and nscans == 1:
        pytest.skip("no extra value in testing")

    # TODO: fix in pymca
    if nscans > 1:
        pytest.skip("fix multi-scan in pymca: issue #978")

    diagnostics = True
    figuresofmerit = True
    quantification = True
    energy = 7.5
    energy_multiplier = 10

    # Generate data
    xrf_spectra_uris, spectra, parameters, config = _generate_data(
        tmpdir, samefile, nscans, npoints_per_scan, energy
    )

    # Output
    output_uri = str(tmpdir / "output.h5::/1.1/fit")
    fit_results_uri = str(tmpdir / "output.h5::/1.1/fit/results")

    # Configuration
    config_filename = str(tmpdir / "config.cfg")
    config.write(config_filename)

    # Perform fit
    with outputbuffer_context(
        output_uri,
        diagnostics=diagnostics,
        figuresofmerit=figuresofmerit,
        output_handler=output_handler,
    ) as output_buffer:
        perform_batch_fit(
            xrf_spectra_uris=xrf_spectra_uris,
            cfg=config_filename,
            output_buffer=output_buffer,
            energy=energy,
            energy_multiplier=energy_multiplier,
            fast=fast,
            quantification=quantification,
        )
        assert output_buffer.fit_results_uri == fit_results_uri

    _validate_results(fit_results_uri, output_handler, fast, parameters, spectra)


def _validate_results(
    fit_results_uri: str,
    output_handler: str,
    fast: bool,
    parameters: Dict[str, numpy.ndarray],
    spectra: numpy.ndarray,
):
    output_file, output_h5path = fit_results_uri.split("::")
    # Validate results
    with h5py.File(output_file, "r") as h5file:
        result_group = h5file[output_h5path]
        nparams = 12
        nobservations = 1021

        # Fit results
        if output_handler == "pymca":
            # includes *_error softlinks
            assert len(result_group["parameters"]) == 2 * nparams
        else:
            assert len(result_group["parameters"]) == nparams
        assert len(result_group["uncertainties"]) == nparams
        for name, values in parameters.items():
            _check_param_dataset(values, name, result_group)

        if output_handler == "pymca":
            spectra = spectra[None, ...]

        # Diagnostics
        if fast:
            assert set(result_group["diagnostics"]) == {
                "nFreeParameters",
                "nObservations",
            }
        else:
            assert set(result_group["diagnostics"]) == {
                "chisq",
                "nFreeParameters",
                "nObservations",
            }
        numpy.testing.assert_array_equal(
            result_group["diagnostics/nFreeParameters"][()], nparams
        )
        numpy.testing.assert_array_equal(
            result_group["diagnostics/nObservations"][()], nobservations
        )

        if fast:
            if output_handler == "pymca":
                # + channels and energy
                assert len(result_group["derivatives"]) == nparams + 2
            else:
                # + energy
                assert len(result_group["derivatives"]) == nparams + 1

        # Fit
        if output_handler == "pymca":
            expected = {
                "data",
                "model",
                "residuals",
                "energy",
                "channels",
                "dim0",
                "dim1",
            }
        else:
            expected = {"data", "model", "residuals", "energy"}
        assert set(result_group["fit"]) == expected
        spectra2 = result_group["fit/data"][()]
        if output_handler == "pymca":
            numpy.testing.assert_allclose(spectra, spectra2, atol=1e-10)
        else:
            numpy.testing.assert_array_equal(spectra, spectra2)
        model = result_group["fit/model"][()]

        residuals = result_group["fit/residuals"][()]
        residuals2 = spectra - model
        mask = ~numpy.isnan(model)
        if output_handler == "pymca":
            if not fast:
                residuals2 = -residuals2
            numpy.testing.assert_allclose(residuals[mask], residuals2[mask], atol=1e-4)
        else:
            numpy.testing.assert_allclose(residuals[mask], residuals2[mask])


def _generate_data(
    tmpdir, samefile: bool, nscans: int, npoints_per_scan: int, energy: float
) -> Tuple[List[str], numpy.ndarray, numpy.ndarray, dict]:
    xrf_spectra_uris = list()
    parameters = dict()
    spectra = list()

    for scan, uri in enumerate(_generate_uris(tmpdir, samefile, nscans), 1):
        spectra_filename, spectra_dsetname = uri.split("::")
        with h5py.File(spectra_filename, "a") as h5file:
            linegroups = [
                EmissionLineGroup(
                    "Si", "K", _generate_counts(300, npoints_per_scan, scan)
                ),
                EmissionLineGroup(
                    "Al", "K", _generate_counts(400, npoints_per_scan, scan)
                ),
                EmissionLineGroup(
                    "Cl", "K", _generate_counts(200, npoints_per_scan, scan)
                ),
                EmissionLineGroup(
                    "Pb", "M", _generate_counts(500, npoints_per_scan, scan)
                ),
                EmissionLineGroup(
                    "P", "K", _generate_counts(200, npoints_per_scan, scan)
                ),
                EmissionLineGroup(
                    "S", "K", _generate_counts(600, npoints_per_scan, scan)
                ),
                EmissionLineGroup(
                    "Ca", "K", _generate_counts(500, npoints_per_scan, scan)
                ),
                EmissionLineGroup(
                    "Ti", "K", _generate_counts(400, npoints_per_scan, scan)
                ),
                EmissionLineGroup(
                    "Ce", "L", _generate_counts(500, npoints_per_scan, scan)
                ),
                EmissionLineGroup(
                    "Fe", "K", _generate_counts(1000, npoints_per_scan, scan)
                ),
            ]
            scattergroups = [
                ScatterLineGroup(
                    "Peak000", _generate_counts(100, npoints_per_scan, scan)
                ),
                ScatterLineGroup(
                    "Compton000", _generate_counts(100, npoints_per_scan, scan)
                ),
            ]
            _spectra, config = xrf_spectra(linegroups, scattergroups, energy=energy)

            h5file[spectra_dsetname] = _spectra

            xrf_spectra_uris.append(uri)
            spectra.extend(_spectra)
            for group in linegroups:
                lst = parameters.setdefault(f"{group.element}_{group.name}", list())
                lst.extend(group.counts)
            for group in scattergroups:
                lst = parameters.setdefault(f"{group.prefix}_{group.name}", list())
                lst.extend(group.counts)

    # Flat list of spectra and peak areas for all points in all scans
    spectra = numpy.asarray(spectra)
    parameters = {name: numpy.asarray(values) for name, values in parameters.items()}
    return xrf_spectra_uris, spectra, parameters, config


def _generate_uris(tmpdir, samefile: bool, nscans: int) -> Iterator[str]:
    if samefile:
        for scan in range(1, nscans + 1):
            yield str(tmpdir / f"spectra.h5::/{scan}.1/measurement/detector")
    else:
        for scan in range(1, nscans + 1):
            yield str(tmpdir / f"spectra{scan}.h5::/{scan}.1/measurement/detector")


def _generate_counts(start_counts: int, npoints_per_scan: int, scan: int) -> List[int]:
    step = 50
    total_step = npoints_per_scan * step
    start = start_counts + (scan - 1) * total_step
    stop = start + total_step
    return list(range(start, stop, step))


def _check_param_dataset(expected_counts, dset_name, result_group):
    fit_counts = result_group[f"parameters/{dset_name}"][()]
    if expected_counts.size < 10:
        # TODO: does not always work. Weights are disabled but even when they are enabled, it does not work.
        fit_errors = 3 * result_group[f"uncertainties/{dset_name}"][()]
        diff = numpy.abs(fit_counts - expected_counts)
        assert (diff < fit_errors).all()
    diff = numpy.abs(numpy.diff(fit_counts) - 50)
    assert (diff < 5).all()
