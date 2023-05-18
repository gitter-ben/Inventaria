"""!
@file groups_and_boxes.py
@brief Defines the inspector for the groups and boxes inventory type

@section todo_groups_and_boxes TODO
- Reimplement everything but with doxygen comments and cleaned up
- Implement PyQt QTests with automatic GUI testing
"""

from PyQt5.Qt import QPalette, QColor, pyqtSlot
from PyQt5.QtWidgets import QSplitter

from .editor import GroupsAndBoxesEditor
from .common import GroupAndBoxIDs
from .navbar import NavBars
from .database import GroupsAndBoxesDatabase
from .groups_and_boxes_signal_master import GroupsAndBoxesSignalMaster


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

        self._signal_master = sig_master  # Acquire singleton instance of signal master
        self._db = database

        self.__setup_gui()  # Set up the GUI

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
        self._navBars = NavBars(self._signal_master)
        self.addWidget(self._navBars)

        self._signal_master.new_group.connect(self._new_group_slot)
        self._signal_master.new_box.connect(self._new_box_slot)

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

        # ================ Set up database ====================
        # Database signals
        self._signal_master.save_state_changed.connect(self._save_state_changed_slot)
        # =====================================================

        # ================= Finish layout =====================
        # h_splitter.setSizes([???])
        # self.setLayout(h_splitter)
        # =====================================================

    @pyqtSlot(int, str)
    def _group_name_changed_slot(self, group_id: int, name: str) -> None:
        print(f"Group (ID: {group_id}) changed name to '{name}'.")

    @pyqtSlot(int, str)
    def _box_name_changed_slot(self, box_id: int, name: str) -> None:
        print(f"Box (ID: {box_id}) changed name to '{name}'.")

    @pyqtSlot(int, str)
    def _group_description_changed_slot(self, group_id: int, new_description: str) -> None:
        print(f"Group (ID: {group_id}) changed its description to '{new_description}'.")

    @pyqtSlot(int, str)
    def _box_description_changed_slot(self, box_id: int, new_description: str) -> None:
        print(f"Box (ID: {box_id}) changed its description to '{new_description}'.")

    @pyqtSlot()
    def _new_group_slot(self) -> None:
        print(f"Add a new group.")

    @pyqtSlot(int)
    def _delete_group_slot(self, group_id: int) -> None:
        print(f"Group (ID: {group_id}) was deleted.")

    @pyqtSlot(int)
    def _new_box_slot(self, group_id: int) -> None:
        print(group_id)
        print(f"Add new box in group (ID: {group_id}).")

    @pyqtSlot(int)
    def _delete_box_slot(self, box_id: int) -> None:
        print(f"Box (ID: {box_id}) was deleted.")

    @pyqtSlot(int)
    def _add_box_contents_slot(self, box_id: int) -> None:
        print(f"Add new box content in box (ID: {box_id}).")

    @pyqtSlot(int, int)
    def _set_box_content_count_slot(self, box_content_id: int, count: int) -> None:
        print(f"Box content (ID: {box_content_id}) set to {count}.")

    @pyqtSlot(bool)
    def _save_state_changed_slot(self, save_state: bool) -> None:
        print(f"Database changed save state to {save_state}.")

    @pyqtSlot(GroupAndBoxIDs)
    def _navbar_selection_changed(self, new_selection: GroupAndBoxIDs) -> None:
        print(f"The navbar selection changed to: {new_selection}")
