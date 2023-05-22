from PyQt5.Qt import pyqtSignal


class SignalMasterBase:
    # Database signal
    save_state_changed = pyqtSignal(bool)
