"""!
@file custom_widgets.py
@brief Contains all the custom widgets needed for the groups_and_boxes inventory type

@section custom_widgets_classes CLASSES
- Editor
"""

from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QLineEdit,
    QPlainTextEdit,
    QListWidget,
    QListWidgetItem
)
from PyQt5.Qt import (
    QIcon,
)
from PyQt5.QtCore import (
    Qt
)

from .common import *
from .groups_and_boxes_signal_master import GroupsAndBoxesSignalMaster
from .database import GroupsAndBoxesDatabase
from code_refactor_src.core.constants import *


class GroupsAndBoxesEditor(QWidget):
    """!
    @brief A class to describe the editor GUI for the groups and boxes inventory type
    """

    def __init__(self, *args, **kw):
        """!
        Initializes a new Editor instance.
        Steps:
        1. Initialize superclass QWidget
        2. Create a reference to the GroupsAndBoxesSignalMaster Singleton
        3. Call self.setup_GUI()

        @return A new GroupsAndBoxesEditor instance
        """
        super(GroupsAndBoxesEditor, self).__init__(*args, **kw)

        self._box = None
        self._group = None
        self._editorState = GroupsAndBoxesEditorMode.EMPTY

        self._signal_master = GroupsAndBoxesSignalMaster()

        self.__setup_vars()
        self.__setup_gui()

    def set_group_info(self, group):
        """!
        Sets the editor to display a group

        @param group: A group instance with info from the DB
        """
        self._group = group
        self._box = None
        self._editorState = GroupsAndBoxesEditorMode.GROUP

        self._description.setPlainText(self._group.description)

        self._headline.setText(f"Group Editor: {self._group.name} (ID: {self._group.id})")

    def set_box_info(self, box):
        """!
        Sets the editor to display a box

        @param box: A box instance with info from the DB
        """
        self._box = box
        self._group = None
        self._editorState = GroupsAndBoxesEditorMode.BOX

        self._description.setPlainText(self._box.description)

        self._headline.setText(f"Box Editor: {self._box.name} (ID: {self._box.id})")

    def set_empty(self):
        """!
        Empties the editor
        """
        self._group = None
        self._box = None
        self._editorState = GroupsAndBoxesEditorMode.EMPTY

        self._headline.setText(f"Editor: No box/group selected")

    def __setup_vars(self):
        self._editorState = GroupsAndBoxesEditorMode.EMPTY
        self._group = None
        self._box = None

    def __setup_gui(self):
        """!
        Sets up the GUI for the Editor.
        Steps:
        1. Initialize the main layout
        2. Make a headline
        3. Make a change name field and button
        4. Make a description box

        Result:
        
         ______________________________________
        |                                      |
        |  Inspector:   Some name (ID: x)      |
        |                           _________  |
        |   Change name: _________ |_change__| |
        |                                      |
        |   Description:                       |
        |   ___________                        |
        |  |           |                       |
        |  |           |                       |
        |  |___________|                       |
        |                                      | 
        |   Component/Box List:                |
        |   ________________________           |
        |  |                        |          |
        |  |                        |          |
        |  |                        |          |
        |  |________________________|          |
        |                                      |
        |                            Delete    |
        |______________________________________|

        """

        # ========== Make the layout ===========
        self._layout = QGridLayout()
        # ======================================

        # ========== Make the headline =========
        self._headline = QLabel("Inspector")
        font = self._headline.font()
        font.setPointSize(13)
        self._headline.setFont(font)
        self._layout.addWidget(self._headline, 0, 0, 1, 1)
        # ======================================

        # ====== Make the change name field ====
        change_name_label = QLabel("Change name: ")
        self._change_name_line_edit = QLineEdit()
        change_name_button = QPushButton("Change name")
        change_name_layout = QHBoxLayout()
        change_name_layout.addWidget(change_name_label)
        change_name_layout.addWidget(self._change_name_line_edit)
        change_name_layout.addWidget(change_name_button)
        self._layout.addLayout(change_name_layout, 1, 0, 1, 1)

        def _change_name_intern():
            new_name = self._change_name_line_edit.text()
            if len(new_name) == 0:
                return

            if self._editorState == GroupsAndBoxesEditorMode.GROUP:
                if new_name != self._group.name:
                    self._signal_master.group_name_changed.emit(self._group.id, new_name)
            elif self._editorState == GroupsAndBoxesEditor.BOX:
                if new_name != self._box.name:
                    self._signal_master.box_name_changed.emit(self._box.id, new_name)

        change_name_button.clicked.connect(_change_name_intern)
        # ======================================

        # ======== Make description ============
        description_label = QLabel("Description:")
        font = description_label.font()
        font.setPointSize(11)
        description_label.setFont(font)

        self._description = QPlainTextEdit()

        self._layout.addWidget(description_label, 2, 0, 1, 1)
        self._layout.addWidget(self._description, 3, 0, 1, 2)

        def _description_changed_intern():
            new_description = self._description.toPlainText()
            if len(new_description) > MAX_DESCRIPTION_LENGTH:
                self.description.textCursor().deletePreviousChar()
            else:
                if self._editorState == GroupsAndBoxesEditorMode.GROUP:
                    self._signal_master.group_description_changed.emit(self._group.id, new_description)
                elif self._editorState == GroupsAndBoxesEditorMode.BOX:
                    self._signal_master.box_description_changed.emit(self._box.id, new_description)

        self._description.textChanged.connect(_description_changed_intern)
        # ======================================

        # ========= Make boxes list ============
        boxes_label = QLabel("Boxes: ")
        font = boxes_label.font()
        font.setPointSize(11)
        boxes_label.setFont(font)

        ic = QIcon(":/icons/green_plus.png")
        add_box_button = QPushButton("Add box")
        add_box_button.setIcon(ic)
        add_box_button.setFixedWidth(110)
        add_box_button.clicked.connect(self._signal_master.add_box.emit)

        self._boxes_list = self.BoxesList()

        self._layout.addWidget(boxes_label, 7, 0, 1, 1)
        self._layout.addWidget(add_box_button, 7, 1, 1, 1, alignment=Qt.AlignRight)
        self._layout.addWidget(self._boxes_list)
        # ======================================

        # ======== Make components list ========
        pass
        # ======================================

        # ========= Set the layout =============
        self.setLayout(self._layout)
        # ======================================

    class BoxesList(QListWidget):
        """!
        @brief QListWidget with option for delete-, add-, etc buttons.

        A subclass of QListWidget that allows for showing of boxes with delete buttons, add buttons, etc.
        """

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self._items = []

        def clear_items(self):
            self.clear()
            self._items = []

        def populate(self, boxes: [Box]):  # This creates item widgets (BoxesListItem) for all the boxes
            for box in boxes:
                item = QListWidget(self)
                self.addItem(item)
                row = self.BoxesListItem(box)
                self._items.append(row)
                item.setSizeHint(row.minimumSizeHint())
                self.setItemWidget(item, row)

        class BoxesListItem(QWidget):
            """!
            @brief Custom List Widget Item.

            An item widget for a QListWidget that allows for saving box id and custom widgets
            """

            def __init__(self, box: Box, *args, **kwargs):
                """!
                Initialize a new BoxesListItem.

                @param box Box: An instance of the Box class from the database
                """
                super().__init__(*args, **kwargs)

                self.box = box

                row = QGridLayout()
                name_label = QLabel(self.box.name)
                row.addWidget(name_label, 0, 0, 1, 1, alignment=Qt.AlignLeft)
                self.setLayout(row)
