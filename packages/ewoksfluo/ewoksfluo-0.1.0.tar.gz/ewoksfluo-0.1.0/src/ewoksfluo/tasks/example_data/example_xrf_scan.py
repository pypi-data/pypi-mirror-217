import logging

import numpy
import h5py
from ewokscore import Task

from ewoksfluo.tests.data import xrf_spectra, deadtime

logger = logging.getLogger(__name__)


class ExampleXRFScan(
    Task,
    input_names=["output_filename"],
    optional_input_names=[
        "nscans",
        "emission_line_groups",
        "energy",
        "npoints",
        "expo_time",
        "ndetectors",
        "flux",
        "counting_noise",
        "rois",
        "integral_type",
    ],
    output_names=[
        "config",
        "configs",
        "energy",
        "energies",
        "xrf_spectra_uris",
        "xrf_spectra_uri",
        "normalize_uris",
        "normalize_reference_values",
        "livetime_uris",
        "livetime_reference_value",
        "I0_uris",
        "I0_reference_values",
        "scan_uri",
        "scan_uris",
        "detector_name",
        "detector_names",
        "xrf_spectra_uri_template",
        "livetime_uri_template",
    ],
):
    def run(self):
        emission_line_groups = self.get_input_value("emission_line_groups", [])
        emission_line_groups = [s.split("-") for s in emission_line_groups]
        energy = self.get_input_value("energy", 12.0)
        nscans = self.get_input_value("nscans", 1)
        scan_numbers = range(1, nscans + 1)
        npoints = self.get_input_value("npoints", 10)
        expo_time = self.get_input_value("expo_time", 0.1)
        ndetectors = self.get_input_value("ndetectors", 1)
        flux = self.get_input_value("flux", 1e7)
        counting_noise = self.get_input_value("counting_noise", True)
        rois = self.get_input_value("rois", list())
        integral_type = self.get_input_value("integral_type", True)
        if integral_type:
            integral_type = numpy.uint32
        else:
            integral_type = None

        I0_reference = int(flux * expo_time)
        I0 = numpy.linspace(
            I0_reference, I0_reference * 0.85, npoints, dtype=numpy.uint32
        )
        efficiency = [1, 2]
        scattergroups = [
            xrf_spectra.ScatterLineGroup(
                "Compton000", (I0 * efficiency[0]).astype(numpy.uint32)
            ),
            xrf_spectra.ScatterLineGroup(
                "Peak000", (I0 * efficiency[1]).astype(numpy.uint32)
            ),
        ]
        efficiency = list(range(3, len(emission_line_groups) + 3))
        linegroups = [
            xrf_spectra.EmissionLineGroup(
                element, group, (I0 * eff).astype(numpy.uint32)
            )
            for eff, (element, group) in zip(efficiency, emission_line_groups)
        ]

        theoretical_spectra, config = xrf_spectra.xrf_spectra(
            linegroups,
            scattergroups,
            energy=energy,
            flux=flux,
            elapsed_time=expo_time,
        )

        measured_data = deadtime.apply_dualchannel_signal_processing(
            theoretical_spectra,
            elapsed_time=expo_time,
            counting_noise=counting_noise,
            integral_type=integral_type,
        )

        roi_data_theory = dict()
        roi_data_cor = dict()
        for i, roi in enumerate(rois, 1):
            roi_name = f"roi{i}"
            idx = Ellipsis, slice(*roi)
            roi_theory = theoretical_spectra[idx].sum(axis=-1) / I0 * I0_reference
            roi_meas = measured_data["spectrum"][idx].sum(axis=-1)
            roi_cor = (
                roi_meas / I0 * I0_reference / measured_data["live_time"] * expo_time
            )
            roi_data_theory[roi_name] = roi_theory
            roi_data_cor[roi_name] = roi_cor
            measured_data[roi_name] = roi_meas

        with h5py.File(self.inputs.output_filename, "a") as nxroot:
            for scan_number in scan_numbers:
                scan_name = f"{scan_number}.1"
                nxroot.attrs["NX_class"] = "NXroot"
                nxroot.attrs["creator"] = "ewoksfluo"

                nxentry = nxroot.require_group(scan_name)
                nxentry.attrs["NX_class"] = "NXentry"
                title = f"loopscan {npoints} {expo_time}"
                if "title" in nxentry:
                    del nxentry["title"]
                nxentry["title"] = title

                nxinstrument = nxentry.require_group("instrument")
                nxinstrument.attrs["NX_class"] = "NXinstrument"
                measurement = nxentry.require_group("measurement")
                measurement.attrs["NX_class"] = "NXcollection"

                nxprocess = nxentry.require_group("theory")
                nxprocess.attrs["NX_class"] = "NXprocess"
                nxnote = nxprocess.require_group("configuration")
                nxnote.attrs["NX_class"] = "NXnote"
                if "data" in nxnote:
                    del nxnote["data"]
                if "type" in nxnote:
                    del nxnote["type"]
                nxnote["type"] = "application/pymca"
                nxnote["data"] = config.tostring()

                nxdata = nxprocess.require_group("elements")
                nxdata.attrs["NX_class"] = "NXdata"
                signals = {
                    f"{g.element}-{g.name}": g.counts / I0 * I0_reference
                    for g in linegroups
                }
                signals.update(
                    {g.name: g.counts / I0 * I0_reference for g in scattergroups}
                )
                names = list(signals)
                nxdata.attrs["signal"] = names[0]
                nxdata.attrs["auxiliary_signals"] = names[1:]
                for k, v in signals.items():
                    if k in nxdata:
                        del nxdata[k]
                    nxdata[k] = v

                if roi_data_theory:
                    nxdata = nxprocess.require_group("rois")
                    nxdata.attrs["NX_class"] = "NXdata"
                    names = list(roi_data_theory)
                    nxdata.attrs["signal"] = names[0]
                    nxdata.attrs["auxiliary_signals"] = names[1:]
                    for k, v in roi_data_theory.items():
                        if k in nxdata:
                            del nxdata[k]
                        nxdata[k] = v

                if roi_data_cor:
                    nxdata = nxprocess.require_group("rois_corrected")
                    nxdata.attrs["NX_class"] = "NXdata"
                    names = list(roi_data_cor)
                    nxdata.attrs["signal"] = names[0]
                    nxdata.attrs["auxiliary_signals"] = names[1:]
                    for k, v in roi_data_cor.items():
                        if k in nxdata:
                            del nxdata[k]
                        nxdata[k] = v

                nxdetector = nxinstrument.require_group("I0")
                nxdetector.attrs["NX_class"] = "NXdetector"
                if "data" in nxdetector:
                    del nxdetector["data"]
                nxdetector["data"] = I0
                if "I0" not in measurement:
                    measurement["I0"] = h5py.SoftLink(nxdetector["data"].name)

                for i in range(ndetectors):
                    det_name = f"mca{i}"
                    nxdetector = nxinstrument.require_group(det_name)
                    nxdetector.attrs["NX_class"] = "NXdetector"
                    for k, v in measured_data.items():
                        if k in nxdetector:
                            del nxdetector[k]
                        nxdetector[k] = v
                        if k == "spectrum":
                            if "data" not in nxdetector:
                                nxdetector["data"] = h5py.SoftLink("spectrum")
                            meas_name = det_name
                        else:
                            meas_name = f"{det_name}_{k}"
                        if meas_name not in measurement:
                            measurement[meas_name] = h5py.SoftLink(nxdetector[k].name)

            config = f"{nxroot.filename}::{nxnote['data'].name}"
            self.outputs.config = config
            self.outputs.configs = [config] * ndetectors
            self.outputs.energy = energy
            self.outputs.energies = [energy] * nscans
            xrf_spectra_uris = [
                f"{nxroot.filename}::/{scan_number}.1/measurement/mca{i}"
                for scan_number in scan_numbers
                for i in range(ndetectors)
            ]
            self.outputs.xrf_spectra_uris = xrf_spectra_uris
            self.outputs.xrf_spectra_uri = xrf_spectra_uris[0]

            self.outputs.normalize_uris = [
                f"{nxroot.filename}::/{scan_number}.1/measurement/{dset_uri}"
                for scan_number in scan_numbers
                for dset_uri in ["I0", "mca0_live_time"]
            ]
            self.outputs.normalize_reference_values = [
                I0_reference,
                expo_time,
            ]
            self.outputs.livetime_uris = [
                f"{nxroot.filename}::/{scan_number}.1/measurement/mca{i}_live_time"
                for scan_number in scan_numbers
                for i in range(ndetectors)
            ]
            self.outputs.livetime_reference_value = expo_time
            self.outputs.I0_uris = [
                f"{nxroot.filename}::/{scan_number}.1/measurement/I0"
                for scan_number in scan_numbers
            ]
            self.outputs.I0_reference_values = [I0_reference] * nscans

            scan_uris = [
                f"{nxroot.filename}::/{scan_number}.1" for scan_number in scan_numbers
            ]
            self.outputs.scan_uris = scan_uris
            self.outputs.scan_uri = scan_uris[0]
            detector_names = [f"mca{i}" for i in range(ndetectors)]
            self.outputs.detector_names = detector_names
            self.outputs.detector_name = detector_names[0]
            self.outputs.xrf_spectra_uri_template = "measurement/{detector_name}"
            self.outputs.livetime_uri_template = "measurement/{detector_name}_live_time"
