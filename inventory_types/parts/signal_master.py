from PyQt5.Qt import pyqtSignal

from invtype_bases.signal_master_base import SignalMasterBase


class PartsSignalMaster(SignalMasterBase):
    # GUI Signals
    delete_part = pyqtSignal(int)
