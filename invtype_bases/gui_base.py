from typing import Type

from PyQt5.QtWidgets import QWidget

from . import DatabaseBase, SignalMasterBase


class GUIBase(QWidget):
    def __init__(
            self,
            db: DatabaseBase,
            sig_master: SignalMasterBase) -> None:

        super().__init__()

        self._db = db
        self._sig_master = sig_master
