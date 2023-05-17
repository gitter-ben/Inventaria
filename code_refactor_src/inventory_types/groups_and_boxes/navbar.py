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

from .groups_and_boxes_signal_master import GroupsAndBoxesSignalMaster


class NavBar(QWidget):
    """!
    @brief NavBar widget for groups and boxes inventory type.

    Consists of two nav bars:
      - group_level_nav
      - box_level_nav
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._signal_master = GroupsAndBoxesSignalMaster()

        self.__setup_gui()

    def __setup_gui(self) -> None:
        """!
        @brief Sets up the GUI.

        Steps:
        1.
        """
