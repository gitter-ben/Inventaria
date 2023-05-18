from PyQt5.Qt import QObject, pyqtSignal


class MainSignalMaster(QObject):
    """!
    @brief Signal master for the main window and database.
    """
    global_save_state_changed = pyqtSignal(bool)
