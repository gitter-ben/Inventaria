"""!
@file gui.py
@brief Defines the GUI for the groups and boxes inventory type.
"""
from PyQt5.Qt import QPalette, QColor, pyqtSlot
from PyQt5.QtWidgets import (
    QSplitter,
    QMessageBox,
    QInputDialog
)

from .constants import INITIAL_WIDTH
from .database import GroupsAndBoxesDatabase
from .editor import GroupsAndBoxesEditor
from .signal_master import GroupsAndBoxesSignalMaster
from .navbar import GroupsAndBoxesNavBars


class GroupsAndBoxesGUI(QSplitter):
    def __init__(
            self,
            database: GroupsAndBoxesDatabase,
            sig_master: GroupsAndBoxesSignalMaster,
            *args,
            **kwargs):
        """!
        Initializes a new inspector for the groups and boxes inventory type.

        Notes:
            - Class inherits from QSplitter to simplify GUI code

        Steps:
        1. Initializes the QWidget superclass
        2. Acquire a Singleton instance of the GroupsAndBoxesSignalMaster class
        3. Calls the setup_gui function to set up the GUI

        @param database: An instance of the GroupsAndBoxesDatabase class

        @return  A new GroupsAndBoxes object
        """

        super(GroupsAndBoxesGUI, self).__init__(*args, **kwargs)  # Initialize QWidget superclass

        self._signal_master = sig_master
        self._db = database

        self.__setup_gui()  # Set up the GUI

    def refresh(self) -> None:
        self._editor.set_empty()
        self._navBars.box_level_nav.clear_items()
        self._navBars.group_level_nav.clear_items()
        self._navBars.group_level_nav.populate(self._db.get_groups())

    def __setup_gui(self) -> None:
        """!
        Sets up the entire GUI for the groups and boxes inspector.
        Steps:
        1. Set up central splitter and layout
        2. Set up colors and stylesheets
        3. Set up nav bars and signals
        4. Set up editor and signals
        5. Set up database signals
        5. Finish layout setup
        """

        # ============== Setup central splitter ===============
        self.setChildrenCollapsible(False)
        # =====================================================

        # ========== Setup colors and stylesheets==============
        # Set the QSplitter handles to a gray
        self.setStyleSheet("QSplitter::handle { background-color: #AAAAAA }")

        # Set background color to (200, 200, 200)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(200, 200, 200))
        self.setPalette(palette)
        # =====================================================

        # ================== Setup nav bars ====================
        self._navBars = GroupsAndBoxesNavBars(self._signal_master)
        self._navBars.group_level_nav.populate(self._db.get_groups())
        self.addWidget(self._navBars)

        self._signal_master.new_group.connect(self._new_group_slot)
        self._signal_master.new_box.connect(self._new_box_slot)

        self._signal_master.navbar_group_selection_changed.connect(self._navbar_group_selection_changed)
        self._signal_master.navbar_box_selection_changed.connect(self._navbar_box_selection_changed)
        # ======================================================

        # =================== Setup editor =====================
        # Instantiate a new editor and connect signals
        # Editor signals
        self._editor = GroupsAndBoxesEditor(self._signal_master)
        self.addWidget(self._editor)

        self._signal_master.group_name_changed.connect(self._group_name_changed_slot)
        self._signal_master.box_name_changed.connect(self._box_name_changed_slot)

        self._signal_master.group_description_changed.connect(self._group_description_changed_slot)
        self._signal_master.box_description_changed.connect(self._box_description_changed_slot)

        self._signal_master.delete_group.connect(self._delete_group_slot)
        self._signal_master.delete_box.connect(self._delete_box_slot)

        self._signal_master.add_box.connect(self._new_box_slot)
        self._signal_master.add_box_content.connect(self._add_box_contents_slot)

        self._signal_master.set_box_content_count.connect(self._set_box_content_count_slot)
        # =====================================================

        # ================= Finish layout =====================
        self.setSizes([INITIAL_WIDTH//3, 2 * INITIAL_WIDTH//3])
        # =====================================================

    @pyqtSlot(int, str)
    def _group_name_changed_slot(self, group_id: int, new_name: str) -> None:
        self._db.edit_group_name(group_id, new_name)
        self._editor.set_group_info(
            self._db.get_group(group_id),
            self._db.get_boxes(group_id)
        )
        self._navBars.group_level_nav.clear_items()
        self._navBars.group_level_nav.populate(self._db.get_groups())
        self._navBars.group_level_nav.set_selected_item_by_id(group_id)
        print(f"Group (ID: {group_id}) changed name to '{new_name}'.")

    @pyqtSlot(int, str)
    def _box_name_changed_slot(self, box_id: int, new_name: str) -> None:
        self._db.edit_box_name(box_id, new_name)
        self._editor.set_box_info(
            self._db.get_box(box_id),
            self._db.get_box_contents(box_id)
        )
        current_group_id = self._navBars.current_ids().group_id
        self._navBars.box_level_nav.clear_items()
        self._navBars.box_level_nav.populate(self._db.get_boxes(current_group_id))
        self._navBars.box_level_nav.set_selected_item_by_id(box_id)
        print(f"Box (ID: {box_id}) changed name to '{new_name}'.")

    @pyqtSlot(int, str)
    def _group_description_changed_slot(self, group_id: int, new_description: str) -> None:
        self._db.edit_group_description(group_id, new_description)
        print(f"Group (ID: {group_id}) changed its description to '{new_description}'.")

    @pyqtSlot(int, str)
    def _box_description_changed_slot(self, box_id: int, new_description: str) -> None:
        self._db.edit_box_description(box_id, new_description)
        print(f"Box (ID: {box_id}) changed its description to '{new_description}'.")

    @pyqtSlot()
    def _new_group_slot(self) -> None:
        name, ok = QInputDialog.getText(self, "New Group", "Name:  ")
        if ok:
            if len(name) == 0:
                self.showMessage("Error", "Name must be at least one letter!")
            else:
                self._db.add_group(name)
                itemid: int = self._navBars.current_ids().group_id
                self._navBars.group_level_nav.clear_items()
                self._navBars.group_level_nav.populate(self._db.get_groups())
                if itemid is not None:
                    self._navBars.group_level_nav.set_selected_item_by_id(itemid)
                print(f"Add a new group.")

    @pyqtSlot(int)
    def _delete_group_slot(self, group_id: int) -> None:
        self._db.delete_group(group_id)
        ids = self._navBars.current_ids()
        print(ids, group_id)
        if ids.group_id == group_id:  # If deleting the current group
            self._editor.set_empty()
            self._navBars.box_level_nav.clear_items()
        self._navBars.group_level_nav.clear_items()
        self._navBars.group_level_nav.populate(self._db.get_groups())
        print(f"Group (ID: {group_id}) was deleted.")

    def _new_box_slot(self) -> None:
        ids = self._navBars.current_ids()
        if ids.group_id is None:
            self._show_message("Error", "No group selected.")
            return

        name, ok = QInputDialog.getText(self, "New Box", "Name:  ")
        if ok:
            if len(name) == 0:
                self.showMessage("Error", "Name must be at least one letter!")
            else:
                self._db.add_box(name, ids.group_id)
                self._navBars.box_level_nav.clear_items()
                self._navBars.box_level_nav.populate(self._db.get_boxes(ids.group_id))
                if ids.box_id is not None:
                    self._navBars.box_level_nav.set_selected_item_by_id(ids.box_id)
                else:
                    if ids.group_id is not None:
                        self._editor.set_group_info(
                            self._db.get_group(ids.group_id),
                            self._db.get_boxes(ids.group_id)
                        )

        print(f"Add new box in group (ID: {ids.group_id}).")

    @pyqtSlot(int)
    def _delete_box_slot(self, box_id: int) -> None:
        self._db.delete_box(box_id)
        ids = self._navBars.current_ids()
        if ids.box_id == box_id:  # current box was deleted
            self._editor.set_empty()
            self._editor.set_group_info(
                self._db.get_group(ids.group_id),
                self._db.get_boxes(ids.group_id)
            )
        self._navBars.box_level_nav.clear_items()
        self._navBars.box_level_nav.populate(self._db.get_boxes(ids.group_id))
        print(f"Delete box (ID: {box_id}).")

    @pyqtSlot(int)
    def _add_box_contents_slot(self, box_id: int) -> None:
        print(f"Add new box content in box (ID: {box_id}).")

    @pyqtSlot(int, int)
    def _set_box_content_count_slot(self, box_content_id: int, count: int) -> None:
        self._db.edit_box_contents_count(
            box_content_id,
            count
        )
        ids = self._navBars.current_ids()
        self._editor.set_box_info(
            self._db.get_box(ids.box_id),
            self._db.get_box_contents(ids.box_id)
        )
        print(f"Box content (ID: {box_content_id}) set to {count}.")

    @pyqtSlot()
    def _navbar_group_selection_changed(self) -> None:
        ids = self._navBars.current_ids()
        if ids.group_id is not None:
            self._navBars.box_level_nav.clear_items()
            self._navBars.box_level_nav.populate(self._db.get_boxes(ids.group_id))
            self._editor.set_group_info(
                self._db.get_group(ids.group_id),
                self._db.get_boxes(ids.group_id)
            )
        else:
            self._editor.set_empty()

        print(f"The navbar selection changed to: {self._navBars.current_ids()}")

    @pyqtSlot()
    def _navbar_box_selection_changed(self) -> None:
        ids = self._navBars.current_ids()
        if ids.group_id is not None:
            if ids.box_id is not None:
                self._editor.set_box_info(
                    self._db.get_box(ids.box_id),
                    self._db.get_box_contents(ids.box_id)
                )
            else:
                self._navBars.box_level_nav.clear_items()
                self._navBars.box_level_nav.populate(self._db.get_boxes(ids.group_id))
                self._editor.set_group_info(
                    self._db.get_group(ids.group_id),
                    self._db.get_boxes(ids.group_id)
                )
        else:
            self._editor.set_empty()

        print(f"The navbar selection changed to: {self._navBars.current_ids()}")

    def _show_message(self, title, msg):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(msg)
        dlg.show()
