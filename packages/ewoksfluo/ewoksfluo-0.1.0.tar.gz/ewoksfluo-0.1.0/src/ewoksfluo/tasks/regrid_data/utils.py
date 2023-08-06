from typing import Sequence, Tuple
import h5py
from numpy import ndarray, nan


def get_number_unique(positions: ndarray, tol: float = 1e-3) -> int:
    """
    Gets the number of unique values (motor positions) in a list according to a certain tolerance in O(n^2).
    Default tolerance is 1e-3 as motors positions are expected in mm and variations should be above the um-scale to be considered unique.

    :param positions: List containing the motor positions
    :param tol: Tolerance when checking the uniqueness. If abs(pos1 - pos0) > tol, pos0 and pos1 are considered unique.
    """
    if len(positions) == 0:
        raise TypeError(
            "Number of unique values can only be computed from a non-empty list"
        )

    # Always include the first position
    unique_positions = [positions[0]]
    for pos in positions[1:]:
        is_unique = all(
            [abs(pos - unique_pos) > tol for unique_pos in unique_positions]
        )
        if is_unique:
            unique_positions.append(pos)

    return len(unique_positions)


def find_position_size(scan_uri: str, position_suburi: str) -> int:
    pos_data = get_position_data(scan_uri, position_suburi)
    assert isinstance(pos_data, ndarray)
    return get_number_unique(pos_data)


def get_position_data(scan_uri: str, position_suburi: str):
    scan_filename, scan_h5path = scan_uri.split("::")

    with h5py.File(scan_filename, "r") as scan_file:
        scan_grp = scan_file[scan_h5path]
        assert isinstance(scan_grp, h5py.Group)
        pos_dataset = scan_grp[position_suburi]
        assert isinstance(pos_dataset, h5py.Dataset)
        return pos_dataset[()]


def save_stack_positions(
    parent: h5py.Group,
    dset_name: str,
    shape: Tuple[int, ...],
    scan_uris: Sequence[str],
    position_suburi: str,
):
    dataset = None
    for i_scan, scan_uri in enumerate(scan_uris):
        pos_data = get_position_data(scan_uri, position_suburi)
        if dataset is None:
            dataset = parent.create_dataset(
                dset_name,
                shape=shape,
                dtype=pos_data.dtype,
            )
        dataset[i_scan, ...] = pos_data.reshape(shape[1:])

    return dataset


def reshape_into_virtual_dset(
    original_dset: h5py.Dataset,
    destination_parent: h5py.Group,
    destination_name: str,
    destination_shape: tuple,
):
    layout = h5py.VirtualLayout(shape=destination_shape, dtype=original_dset.dtype)
    vsource = h5py.VirtualSource(
        original_dset.file.filename, original_dset.name, shape=original_dset.shape
    )
    layout[...] = vsource
    destination_parent.create_virtual_dataset(destination_name, layout, fillvalue=nan)
