from datetime import datetime
from typing import Optional, Sequence, Union
import h5py


def create_entry(
    parent: Union[h5py.File, h5py.Group], name: str, default: Optional[str] = None
) -> h5py.Group:
    entry = parent.create_group(name)
    entry.attrs["NX_class"] = "NXentry"
    if default:
        entry.attrs["default"] = default

    return entry


def create_process(
    parent: Union[h5py.File, h5py.Group],
    name: str,
    default: Optional[str] = None,
) -> h5py.Group:
    process = parent.create_group(name)
    process.attrs["NX_class"] = "NXprocess"
    if default:
        process.attrs["default"] = default

    return process


def create_data(
    parent: Union[h5py.File, h5py.Group],
    name: str,
    signal: Optional[str] = None,
) -> h5py.Group:
    nxdata = parent.create_group(name)
    nxdata.attrs["NX_class"] = "NXdata"
    if signal:
        nxdata.attrs["signal"] = signal

    return nxdata


def set_data_signals(nxdata: h5py.Group, signals: Sequence[str]):
    nxdata.attrs["signal"] = signals[0]
    if len(signals) > 1:
        nxdata.attrs["auxiliary_signals"] = signals[1:]


def now() -> str:
    """NeXus-compliant format of the current time"""
    return datetime.now().astimezone().isoformat()
