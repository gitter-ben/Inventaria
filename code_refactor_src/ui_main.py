from PyQt5.Qt import (
    QIcon,
)
from PyQt5.QtCore import (
    Qt
)
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QLineEdit,
    QPlainTextEdit,
    QListWidget,
    QListWidgetItem,
    QSpacerItem,
    QMainWindow
)

from inventory_types.groups_and_boxes import *
from database import MainDatabase


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db = None
        self.db_loaded = False

        self._dbs = []
        self._inventories = []

        self.setup_gui()

    def setup_gui(self) -> None:
        self._dbs.append(GroupsAndBoxesDatabase("groups_and_boxes.sqlite"))
        self._inventories.append(GroupsAndBoxesGUI(self._dbs[-1]))

        self.setCentralWidget(self._inventories[0])
