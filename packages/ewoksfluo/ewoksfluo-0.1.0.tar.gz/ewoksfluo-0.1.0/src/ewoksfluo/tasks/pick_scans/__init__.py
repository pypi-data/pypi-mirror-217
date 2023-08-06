from typing import List, Sequence, Tuple
from ewokscore import Task


class PickScansInFiles(
    Task,
    input_names=["bliss_filenames", "scan_ranges"],
    optional_input_names=["exclude_scans"],
    output_names=["scan_uris"],
):
    def run(self):
        bliss_filenames: Sequence[str] = self.inputs.bliss_filenames
        scan_ranges: Sequence[Tuple[int, int]] = self.inputs.scan_ranges
        exclude_scans: Sequence[Sequence[int]] = self.get_input_values(
            "exclude_scans", []
        )

        scan_uris: List[str] = []
        for bliss_filename, scan_range, excluded_scans in zip(
            bliss_filenames, scan_ranges, exclude_scans
        ):
            scan_min, scan_max = scan_range
            excluded_scans = excluded_scans if excluded_scans else []
            for scan_number in range(scan_min, scan_max + 1):
                if scan_number in excluded_scans:
                    continue

                scan_uris.append(f"{bliss_filename}::/{scan_number}.1")

        self.outputs.scan_uris = scan_uris
