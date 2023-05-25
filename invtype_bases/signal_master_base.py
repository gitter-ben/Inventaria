from PyQt5.Qt import pyqtSignal, QObject


class SignalMasterBase(QObject):
    # Database signal
    save_state_changed = pyqtSignal(bool)
