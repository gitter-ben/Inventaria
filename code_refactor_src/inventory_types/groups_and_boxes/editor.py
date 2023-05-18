"""!
@file editor.py
@brief Contains all the custom widgets needed for the groups_and_boxes inventory type

@section custom_widgets_classes CLASSES
- GroupsAndBoxesEditor (QWidget)
  - BoxesList (QListWidget)
    - BoxesListItem (QWidget)
"""
from typing import List

from PyQt5.Qt import (
    QIcon
)
from PyQt5.QtCore import (
    Qt,
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
    QSpacerItem
)

from code_refactor_src.core.constants import *
from code_refactor_src.resources import resources
from .common import *
from .groups_and_boxes_signal_master import GroupsAndBoxesSignalMaster


class GroupsAndBoxesEditor(QWidget):
    """!
    @brief A class to describe the editor GUI for the groups and boxes inventory type
    """
    def __init__(self, sig_master: GroupsAndBoxesSignalMaster, *args, **kw):
        """!
        Initializes a new Editor instance.
        Steps:
        1. Initialize superclass QWidget
        2. Create a reference to the GroupsAndBoxesSignalMaster Singleton
        3. Call self.setup_GUI()

        @return A new GroupsAndBoxesEditor instance
        """
        super(GroupsAndBoxesEditor, self).__init__(*args, **kw)

        self.nothing(resources.qt_version)  # Make the damn import warning disappear

        self._box = None
        self._group = None
        self._editorState = GroupsAndBoxesEditorMode.EMPTY

        self._signal_master = sig_master

        self.__setup_vars()
        self.__setup_gui()

    @staticmethod
    def nothing(x):
        """!
        This method's sole purpose is the elimination of an unused import warning
        because it can't see that resources/resources.py is being used. Without that
        import the images and icons wouldn't work.
        """
        return x

    def set_group_info(self, group: Group, boxes: List[Box]) -> None:
        """!
        Sets the editor to display a group

        @param group: A group instance with info from the DB
        @param boxes: A list of instances of the Box dataclass
        """
        self._group = group
        self._box = None
        self._editorState = GroupsAndBoxesEditorMode.GROUP

        self._headline.setText(f"Group Editor: {self._group.name} (ID: {self._group.id})")

        self._change_name_line_edit.setText(self._group.name)

        self._description.blockSignals(True)
        self._description.setPlainText(self._group.description)
        self._description.blockSignals(False)

        self._boxes_list.clear_items()
        self._boxes_list.populate(boxes)
        self._box_contents_list.clear_items()

        # Set everything to invisible
        self._change_name_label.setVisible(True)
        self._change_name_line_edit.setVisible(True)
        self._change_name_button.setVisible(True)
        self._description_label.setVisible(True)
        self._description.setVisible(True)
        self._boxes_label.setVisible(True)
        self._boxes_list.setVisible(True)
        self._box_contents_label.setVisible(False)
        self._box_contents_list.setVisible(False)
        self._add_box_button.setVisible(True)
        self._add_box_content_button.setVisible(False)
        self._delete_button.setVisible(True)

    def set_box_info(self, box: Box, box_contents: List[BoxContentItem]) -> None:
        """!
        Sets the editor to display a box

        @param box: A box instance with info from the DB
        @param box_contents: A list of instances of the BoxContentItem dataclass
        """
        self._box = box
        self._group = None
        self._editorState = GroupsAndBoxesEditorMode.BOX

        self._headline.setText(f"Box Editor: {self._box.name} (ID: {self._box.id})")

        self._change_name_line_edit.setText(self._box.name)

        self._description.blockSignals(True)
        self._description.setPlainText(self._box.description)
        self._description.blockSignals(False)

        self._boxes_list.clear_items()
        self._box_contents_list.clear_items()
        self._box_contents_list.populate(box_contents)

        # Set everything to invisible
        self._change_name_label.setVisible(True)
        self._change_name_line_edit.setVisible(True)
        self._change_name_button.setVisible(True)
        self._description_label.setVisible(True)
        self._description.setVisible(True)
        self._boxes_label.setVisible(False)
        self._boxes_list.setVisible(False)
        self._box_contents_label.setVisible(True)
        self._box_contents_list.setVisible(True)
        self._add_box_button.setVisible(False)
        self._add_box_content_button.setVisible(True)
        self._delete_button.setVisible(True)

    def set_empty(self) -> None:
        """!
        @brief Empties the editor.
        """
        self._group = None
        self._box = None
        self._editorState = GroupsAndBoxesEditorMode.EMPTY

        self._headline.setText(f"Editor: No box/group selected")

        self._change_name_line_edit.clear()

        self._description.blockSignals(True)
        self._description.clear()
        self._description.blockSignals(False)

        self._boxes_list.clear_items()
        self._box_contents_list.clear_items()

        # Set everything to invisible
        self._change_name_label.setVisible(False)
        self._change_name_line_edit.setVisible(False)
        self._change_name_button.setVisible(False)
        self._description_label.setVisible(False)
        self._description.setVisible(False)
        self._boxes_label.setVisible(False)
        self._boxes_list.setVisible(False)
        self._box_contents_label.setVisible(False)
        self._box_contents_list.setVisible(False)
        self._add_box_button.setVisible(False)
        self._add_box_content_button.setVisible(False)
        self._delete_button.setVisible(False)

    def __setup_vars(self) -> None:
        self._editorState = GroupsAndBoxesEditorMode.EMPTY
        self._group = None
        self._box = None

    def __setup_gui(self) -> None:
        """!
        Sets up the GUI for the Editor.
        Steps:
        1. Initialize the main layout
        2. Make a headline
        3. Make a change name field and button
        4. Make a description box
        5. Make a spacer
        6. Make a BoxesList
        7. Make a BoxContentsList
        8. Make a button row at the bottom
        9. Set the layout to self

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
        self._layout.setAlignment(Qt.AlignTop)
        # ======================================

        # ========== Make the headline =========
        self._headline = QLabel("Inspector")
        font = self._headline.font()
        font.setPointSize(13)
        self._headline.setFont(font)
        self._layout.addWidget(self._headline, 0, 0, 1, 1)
        # ======================================

        # ====== Make the change name field ====
        self._change_name_label = QLabel("Change name: ")
        self._change_name_line_edit = QLineEdit()
        self._change_name_button = QPushButton("Change name")
        self._change_name_layout = QHBoxLayout()
        self._change_name_layout.addWidget(self._change_name_label)
        self._change_name_layout.addWidget(self._change_name_line_edit)
        self._change_name_layout.addWidget(self._change_name_button)
        self._layout.addLayout(self._change_name_layout, 1, 0, 1, 2)

        def _change_name_intern():
            new_name = self._change_name_line_edit.text()
            if len(new_name) == 0:
                return

            if self._editorState == GroupsAndBoxesEditorMode.GROUP:
                if new_name != self._group.name:
                    self._signal_master.group_name_changed.emit(self._group.id, new_name)
            elif self._editorState == GroupsAndBoxesEditorMode.BOX:
                if new_name != self._box.name:
                    self._signal_master.box_name_changed.emit(self._box.id, new_name)

        self._change_name_button.clicked.connect(_change_name_intern)
        # ======================================

        # ======== Make description ============
        self._description_label = QLabel("Description:")
        font = self._description_label.font()
        font.setPointSize(11)
        self._description_label.setFont(font)

        self._description = QPlainTextEdit()

        self._layout.addWidget(self._description_label, 2, 0, 1, 1)
        self._layout.addWidget(self._description, 3, 0, 1, 2)

        def _description_changed_intern():
            new_description = self._description.toPlainText()
            if len(new_description) > MAX_DESCRIPTION_LENGTH:
                self._description.textCursor().deletePreviousChar()
            else:
                if self._editorState == GroupsAndBoxesEditorMode.GROUP:
                    self._signal_master.group_description_changed.emit(self._group.id, new_description)
                elif self._editorState == GroupsAndBoxesEditorMode.BOX:
                    self._signal_master.box_description_changed.emit(self._box.id, new_description)

        self._description.textChanged.connect(_description_changed_intern)
        # ======================================

        # =========== Add Spacer ===============
        self._layout.addItem(QSpacerItem(10, 25), 4, 0, 1, 2)
        # ======================================

        # ========= Make boxes list ============
        self._boxes_label = QLabel("Boxes: ")
        font = self._boxes_label.font()
        font.setPointSize(11)
        self._boxes_label.setFont(font)

        ic = QIcon(":/icons/green_plus.png")
        self._add_box_button = QPushButton("Add box")
        self._add_box_button.setIcon(ic)
        self._add_box_button.setFixedWidth(110)
        self._add_box_button.clicked.connect(lambda: self._signal_master.add_box.emit(self._group.id))

        self._boxes_list = self.BoxesList(self._signal_master)

        self._layout.addWidget(self._boxes_label, 7, 0, 1, 1)
        self._layout.addWidget(self._add_box_button, 7, 1, 1, 1, alignment=Qt.AlignRight)
        self._layout.addWidget(self._boxes_list, 8, 0, 1, 2)
        # ======================================

        # ======== Make box contents list ========
        self._box_contents_label = QLabel("Contents of box:")
        font = self._box_contents_label.font()
        font.setPointSize(11)
        self._box_contents_label.setFont(font)

        ic = QIcon(":/icons/green_plus.png")
        self._add_box_content_button = QPushButton("Add content item")
        self._add_box_content_button.setIcon(ic)
        self._add_box_content_button.setFixedWidth(180)
        self._add_box_content_button.clicked.connect(lambda: self._signal_master.add_box_content.emit(self._box.id))

        self._box_contents_list = self.BoxContentsList(self._signal_master)

        self._layout.addWidget(self._box_contents_label, 5, 0, 1, 1)
        self._layout.addWidget(self._add_box_content_button, 5, 1, 1, 1, alignment=Qt.AlignRight)
        self._layout.addWidget(self._box_contents_list, 8, 0, 1, 2)
        # ======================================

        # ===== Button row at the bottom =======
        self._button_layout = QHBoxLayout()
        self._button_layout.setAlignment(Qt.AlignRight)
        ic = QIcon(":/icons/delete_icon.png")
        self._delete_button = QPushButton("Delete")
        self._delete_button.setIcon(ic)
        self._delete_button.clicked.connect(
            lambda: self._signal_master.delete_box.emit(self._box.id)
            if self._editorState == GroupsAndBoxesEditorMode.BOX
            else self._signal_master.delete_group.emit(self._group.id)
        )

        self._button_layout.addWidget(self._delete_button)
        self._layout.addLayout(self._button_layout, 9, 0, 1, 2)
        # ======================================

        # ========= Set the layout =============
        self.setLayout(self._layout)
        # ======================================

        # ========= Empty the editor ===========
        self.set_empty()
        # ======================================

    class BoxesList(QListWidget):
        """!
        @brief QListWidget with option for delete-, add-, etc buttons.

        A subclass of QListWidget that allows for showing of boxes with delete buttons, add buttons, etc.
        """

        def __init__(self, sig_master: GroupsAndBoxesSignalMaster, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self._signal_master = sig_master
            self._items = []

        def clear_items(self) -> None:
            self.clear()
            self._items = []

        def populate(self, boxes: List[Box]) -> None:  # This creates item widgets (BoxesListItem) for all the boxes
            for box in boxes:
                item = QListWidgetItem(self)
                self.addItem(item)
                row = self.BoxesListItem(box, self._signal_master)
                self._items.append(row)
                item.setSizeHint(row.minimumSizeHint())
                self.setItemWidget(item, row)

        class BoxesListItem(QWidget):
            """!
            @brief Custom List Widget Item.

            An item widget for a QListWidget that allows for saving box id and custom widgets
            """

            def __init__(self, box: Box, sig_master: GroupsAndBoxesSignalMaster, *args, **kwargs):
                """!
                Initialize a new BoxesListItem.

                @param box Box: An instance of the Box class from the database
                """
                super().__init__(*args, **kwargs)

                self._signal_master = sig_master
                self._box = box

                row = QGridLayout()
                name_label = QLabel(self._box.name)
                row.addWidget(name_label, 0, 0, 1, 1, alignment=Qt.AlignLeft)
                self.setLayout(row)

    class BoxContentsList(QListWidget):
        """!
        @brief Custom list widget with support for BoxContentsListItem

        A subclass of QListWidget that allows for showing of box contents
        with +, - and count labels.
        """
        def __init__(self, sig_master: GroupsAndBoxesSignalMaster, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self._signal_master = sig_master
            self._items = []

        def clear_items(self) -> None:
            self.clear()
            self._items = []

        def populate(self, box_contents: List[BoxContentItem]) -> None:
            for box_content in box_contents:
                item = QListWidgetItem(self)
                self.addItem(item)
                row = self.BoxContentsListItem(box_content, self._signal_master)
                self._items.append(row)
                item.setSizeHint(row.minimumSizeHint())
                self.setItemWidget(item, row)

        class BoxContentsListItem(QWidget):
            """!
            @brief Custom item class for BoxContentsList (QListWidget)

            A custom item for the BoxContentsList class that has a custom GUI:
             _________________________
            | <Name>      + <count> - |
            |_________________________|
            """
            def __init__(self, box_content: BoxContentItem, sig_master: GroupsAndBoxesSignalMaster, *args, **kwargs):
                """!
                Initializes the GUI and signals for the BoxContentsListItem used in BoxContentsList
                """
                super().__init__(*args, **kwargs)

                self._signal_master = sig_master

                self._content = box_content
                self._id = self._content.id

                minus_button = QPushButton("-")
                minus_button.setFixedWidth(30)
                minus_button.clicked.connect(
                    lambda: self._signal_master.set_box_content_count.emit(self._id, self._content.count - 1)
                    if self._content.count > 0 else None
                )  # Emit only if count above 0
                count_label = QLabel(str(self._content.count))
                # count_label = QLineEdit()
                # positive_int_only = QIntValidator()
                # positive_int_only.setBottom(0)
                # count_label.setValidator(positive_int_only)
                # count_label.setText(str(self._content.count))
                # count_label.editingFinished.connect(
                #     lambda: self._signal_master.set_box_content_count.emit(self._id, int(count_label.text()))
                # )
                plus_button = QPushButton("+")
                plus_button.setFixedWidth(30)
                plus_button.clicked.connect(
                    lambda: self._signal_master.set_box_content_count.emit(self._id, self._content.count + 1)
                )  # Lambda to emit signal with argument

                count_layout = QHBoxLayout()
                count_layout.addWidget(minus_button)
                count_layout.addWidget(count_label)
                count_layout.addWidget(plus_button)

                row = QHBoxLayout()
                row.addWidget(QLabel(self._content.name))
                row.addStretch()
                row.addLayout(count_layout)

                self.setLayout(row)
