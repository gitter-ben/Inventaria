from typing import List, Tuple

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

        self._inventories: List[Tuple[GroupsAndBoxesSignalMaster, GroupsAndBoxesDatabase, GroupsAndBoxesGUI], ...] = []

        self.__setup_gui()

    def __setup_gui(self) -> None:
        self._add_inventory()
        self.setCentralWidget(self._inventories[0][2])
        self._inventories[0][2]._editor.set_group_info(
            self._inventories[0][1].get_group(1),
            self._inventories[0][1].get_boxes(1)
        )

    def _add_inventory(self) -> None:
        sig_master = GroupsAndBoxesSignalMaster()
        db = GroupsAndBoxesDatabase("groups_and_boxes.sqlite", sig_master)
        gui = GroupsAndBoxesGUI(db, sig_master)

        self._inventories.append((sig_master, db, gui))
