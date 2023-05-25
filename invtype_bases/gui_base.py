from PyQt5.QtWidgets import QWidget

from .database_base import DatabaseBase
from .signal_master_base import SignalMasterBase


class GUIBase(QWidget):
    def __init__(
            self,
            db: DatabaseBase,
            sig_master: SignalMasterBase) -> None:

        super().__init__()

        self._db = db
        self._signal_master = sig_master
