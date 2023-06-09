"""!
@file navbar.py
@brief Defines the navbar widgets for the groups and boxes inventory type.

@section custom_widgets_classes CLASSES
- GroupsAndBoxesNavBars (QSplitter)
  - NavBar (QListWidget)
    - NavBarItem (QWidget)
"""
from typing import List

from PyQt5.Qt import (
    QIcon,
)
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QGridLayout,
    QListWidget,
    QListWidgetItem,
    QSplitter
)

from .signal_master import GroupsAndBoxesSignalMaster
from .common import Group, Box, GroupAndBoxIDs
from resources import resources


class GroupsAndBoxesNavBars(QSplitter):
    """!
    @brief NavBar widget for groups and boxes inventory type.

    Consists of two nav bars:
      - group_level_nav
      - box_level_nav
    """
    def __init__(self, sig_master: GroupsAndBoxesSignalMaster, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.nothing(resources.qt_version)  # Fix the damn import warning (do something with resources)

        self._signal_master = sig_master
        self.__setup_gui()

    @staticmethod
    def nothing(x):
        """!
        This method's sole purpose is the elimination of an unused import warning
        because it can't see that resources/resources.py is being used even though
        without the import the images and icons wouldn't be loaded.
        """
        return x

    def __setup_gui(self) -> None:
        """!
        @brief Sets up the GUI.

        Notes:
            - Class inherits from QSplitter to simplify GUI code

        Steps:
        1. Setup central splitter
        2. Make group level nav
        3. Make box level nav

        Result:

        <Make GUI>
        """

        # ====== Make central splitter =========
        self.setChildrenCollapsible(False)
        # ======================================

        # ======== Make group level nav ========
        group_level_nav_container = QWidget()
        group_level_nav_layout = QGridLayout()

        group_level_nav_layout.addWidget(group_level_nav_label := QLabel("Groups"), 0, 0, 1, 1)
        font = group_level_nav_label.font()
        font.setPointSize(13)
        group_level_nav_label.setFont(font)

        ic = QIcon(":/icons/green_plus.png")
        new_group_button = QPushButton("New Group")
        new_group_button.setIcon(ic)
        new_group_button.clicked.connect(
            self._signal_master.new_group.emit
        )
        group_level_nav_layout.addWidget(new_group_button, 0, 1, 1, 1)

        # def group_selection_changed_intern():
        #     pass

        self.group_level_nav = self.NavBar(self._signal_master)
        self.group_level_nav.setSortingEnabled(True)
        self.group_level_nav.currentRowChanged.connect(
            self._signal_master.navbar_group_selection_changed.emit
        )
        group_level_nav_layout.addWidget(self.group_level_nav, 1, 0, 1, 2)

        group_level_nav_container.setLayout(group_level_nav_layout)

        self.addWidget(group_level_nav_container)
        # ======================================

        # =========== Box level nav ============
        box_level_nav_container = QWidget()
        box_level_nav_layout = QGridLayout()

        box_level_nav_layout.addWidget(box_level_nav_label := QLabel("Boxes"), 0, 0, 1, 1)
        font = box_level_nav_label.font()
        font.setPointSize(13)
        box_level_nav_label.setFont(font)

        ic = QIcon(":/icons/green_plus.png")
        new_box_button = QPushButton("New Box")
        new_box_button.setIcon(ic)

        new_box_button.clicked.connect(
            self._signal_master.new_box.emit
        )
        box_level_nav_layout.addWidget(new_box_button, 0, 1, 1, 1)

        # def box_selection_changed_intern():
        #     pass

        self.box_level_nav = self.NavBar(self._signal_master)
        self.box_level_nav.setSortingEnabled(True)
        self.box_level_nav.currentRowChanged.connect(
            self._signal_master.navbar_box_selection_changed.emit
        )
        box_level_nav_layout.addWidget(self.box_level_nav, 1, 0, 1, 2)

        box_level_nav_container.setLayout(box_level_nav_layout)

        self.addWidget(box_level_nav_container)
        # ======================================

    def current_ids(self) -> GroupAndBoxIDs:
        """!
        @brief Gets the current ids of the selected group and box.

        @return A NamedTuple (GroupAndBoxIDs) with group_id and box_id fields.
        """
        group = self.group_level_nav.currentItem()
        box = self.box_level_nav.currentItem()
        if group is not None:
            group = group.id
        if box is not None:
            box = box.id
        return GroupAndBoxIDs(group, box)

    class NavBar(QListWidget):
        """!
        @brief A class to represent a navbar.

        An extension of a QListWidget that adds following features:
        1. A custom populate method that takes a list of Group-instances or Box-instances.
        2. A method to select an item from an id.
        """
        def __init__(self, sig_master: GroupsAndBoxesSignalMaster, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._signal_master = sig_master

        def clear_items(self) -> None:
            self.clear()

        def populate(self, items: List[Group | Box]) -> None:
            for item in items:
                self.addItem(self.NavBarItem(item.id, item.name))
            self.sortItems()

        def set_selected_item_by_id(self, item_id: int):
            for i in range(self.count()):
                if self.item(i).id == item_id:
                    self.setCurrentItem(self.item(i))
                    break

        class NavBarItem(QListWidgetItem):
            """!
            @brief Custom QListWidgetItem for the nav bar in the groups and boxes inventory type.
            """
            def __init__(self, item_id, name, *args, **kwargs):
                super().__init__(name, *args, **kwargs)
                self.id = item_id
                self.name = name
