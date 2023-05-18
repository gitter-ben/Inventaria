from PyQt5.Qt import QObject, pyqtSignal


class GlobalSignalMaster(QObject):
    global_save_state_changed = pyqtSignal(bool)
