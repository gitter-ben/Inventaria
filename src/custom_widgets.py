from top_level_boxes_hierarchy import *
from PyQt5 import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from constants import *
import sys
import resources

class Inspector(QWidget):
    descriptionChanged = pyqtSignal(int, str)
    addBox = pyqtSignal()
    deleteBox = pyqtSignal(int)
    deleteGroup = pyqtSignal(int)
    changeBoxName = pyqtSignal(int, str)
    changeGroupName = pyqtSignal(int, str)

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        super_layout = QGridLayout()

        self.headline = QLabel("Inspector")
        font = self.headline.font()
        font.setPointSize(13)
        self.headline.setFont(font)

        self.change_name_label = QLabel("Change name: ")
        self.change_name_line_edit = QLineEdit()
        self.change_name_button = QPushButton("Change name")
        self.change_name_button.pressed.connect(self._changeNameIntern)

        self.description_label = QLabel("Description: ")
        font = self.description_label.font()
        font.setPointSize(11)
        self.description_label.setFont(font)

        self.description = QPlainTextEdit()
        self.description.textChanged.connect(self._descriptionChangedIntern)
        
        self.boxes_label = QLabel("Boxes: ")
        font = self.boxes_label.font()
        font.setPointSize(11)
        self.boxes_label.setFont(font)
        ic = QIcon(":/icons/green_plus.png")
        self.add_box_button = QPushButton("Add Box")
        self.add_box_button.setIcon(ic)
        self.add_box_button.setFixedWidth(110)
        self.add_box_button.pressed.connect(self._addBoxIntern)
        self.boxes_list = BoxesList()

        self.components_label = QLabel("Components: ")
        font = self.components_label.font()
        font.setPointSize(11)
        self.components_label.setFont(font)
        ic = QIcon(":/icons/green_plus.png")
        self.add_component_button = QPushButton("Add Comp.")
        self.add_component_button.setIcon(ic)
        self.add_component_button.setFixedWidth(110)
        self.add_component_button.pressed.connect(self._addComponentIntern)
        self.components_list = ComponentsList()

        self.buttoncontainer = QWidget()
        button_layout = QGridLayout()
        button_layout.setAlignment(Qt.AlignRight)
        ic = QIcon(":/icons/delete_icon.png")
        self.delete_button = QPushButton("Delete")
        self.delete_button.setIcon(ic)
        self.delete_button.pressed.connect(self._deleteButtonPressedIntern)
        button_layout.addWidget(self.delete_button, 0, 0, 1, 1)
        self.buttoncontainer.setLayout(button_layout)

        super_layout.setAlignment(Qt.AlignTop)
        super_layout.addWidget(self.headline, 0, 0, 1, 1)
        self.change_name_container = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.change_name_label)#, 1, 0, 1, 1)
        layout.addWidget(self.change_name_line_edit)#, 1, 1, 1, 1)
        layout.addWidget(self.change_name_button)#, 1, 2, 1, 1)
        self.change_name_container.setLayout(layout)
        super_layout.addWidget(self.change_name_container, 1, 0, 1, 1)

        super_layout.addWidget(self.description_label, 2, 0, 1, 1)
        super_layout.addWidget(self.description, 3, 0, 1, 2)
        
        super_layout.addItem(QSpacerItem(10, 25), 4, 0, 1, 2)

        super_layout.addWidget(self.components_label, 5, 0, 1, 1)
        super_layout.addWidget(self.add_component_button, 5, 1, 1, 1, alignment=Qt.AlignRight)
        super_layout.addWidget(self.components_list, 6, 0, 1, 2)

        super_layout.addWidget(self.boxes_label, 7, 0, 1, 1)
        super_layout.addWidget(self.add_box_button, 7, 1, 1, 1, alignment=Qt.AlignRight)
        super_layout.addWidget(self.boxes_list, 8, 0, 1, 2)
        
        super_layout.addWidget(self.buttoncontainer, 9, 0, 1, 2)

        self.setLayout(super_layout)
        self.empty()

    def _addBoxIntern(self):
        self.addBox.emit()

    def _addComponentIntern(self):
        pass

    def _changeNameIntern(self):
        if len(self.change_name_line_edit.text()) == 0:
            return

        if self.group_box_or_empty == GROUP:
            if self.change_name_line_edit.text() != self.group.name:
                self.changeGroupName.emit(self.group.id, self.change_name_line_edit.text())
        elif self.group_box_or_empty == BOX:
            if self.change_name_line_edit.text() != self.box.name:
                self.changeBoxName.emit(self.box.id, self.change_name_line_edit.text())

    def _descriptionChangedIntern(self):
        if len(self.description.toPlainText()) > MAX_DESCRIPTION_LENGTH:
            self.description.textCursor().deletePreviousChar()
        else:
            self.descriptionChanged.emit(self.group_box_or_empty, self.description.toPlainText())

    def _deleteButtonPressedIntern(self):
        if self.group_box_or_empty == GROUP:
            self.deleteGroup.emit(self.group.id)
        elif self.group_box_or_empty == BOX:
            self.deleteBox.emit(self.box.id)

    def empty(self):
        self.group = None
        self.box = None

        self.headline.setText("Inspector: No box/group selected")
        
        self.description.blockSignals(True)
        self.description.clear()
        self.description.blockSignals(False)

        self.components_list.clear_items()
        self.boxes_list.clear_items()
        self.boxes_label.setVisible(False)
        self.boxes_list.setVisible(False)
        self.components_label.setVisible(False)
        self.components_list.setVisible(False)
        self.description_label.setVisible(False)
        self.description.setVisible(False)
        self.buttoncontainer.setVisible(False)
        self.add_box_button.setVisible(False)
        self.add_component_button.setVisible(False)
        self.change_name_container.setVisible(False)
        self.change_name_line_edit.clear()
        self.group_box_or_empty = EMPTY

    def setGroupInfo(self, group: Group, boxes):
        self.group = group
        self.box = None

        self.headline.setText(f"Group Inspector: {group.name} (ID: {group.id})")

        self.description.blockSignals(True)
        self.description.setPlainText(group.description)
        self.description.blockSignals(False)
        
        self.boxes_list.clear_items()
        #self.boxes_list.populate([(Component(5, "test 1"), 5), (Component(6, "test 2"), 1), (Component(3, "test 3"), 10)])
        self.boxes_list.populate(boxes)

        self.components_label.setVisible(False)
        self.components_list.setVisible(False)
        self.boxes_label.setVisible(True)
        self.boxes_list.setVisible(True)
        self.description_label.setVisible(True)
        self.description.setVisible(True)
        self.buttoncontainer.setVisible(True)
        self.add_box_button.setVisible(True)
        self.add_component_button.setVisible(False)
        self.change_name_container.setVisible(True)
        self.change_name_line_edit.clear()
        self.group_box_or_empty = GROUP

    def setBoxInfo(self, box: Box, components):
        self.box = box
        self.group = None

        self.headline.setText(f"Box Inspector: {box.name} (ID: {box.id})")

        self.description.blockSignals(True)
        self.description.setPlainText(box.description)
        self.description.blockSignals(False)
        
        self.components_list.clear_items()
        #self.components_list.populate([(Component(5, "test 1"), 5), (Component(6, "test 2"), 1), (Component(3, "test 3"), 10)])
        self.components_list.populate(components)
        self.boxes_label.setVisible(False)
        self.boxes_list.setVisible(False)
        self.components_label.setVisible(True)
        self.components_list.setVisible(True)
        self.description_label.setVisible(True)
        self.description.setVisible(True)
        self.buttoncontainer.setVisible(True)
        self.add_box_button.setVisible(False)
        self.add_component_button.setVisible(True)
        self.change_name_container.setVisible(True)
        self.change_name_line_edit.clear()
        self.group_box_or_empty = BOX

class ComponentsList(QListWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.items = []
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
    
    def clear_items(self):
        self.clear()
        self.items = []

    def populate(self, parts):
        for part in parts:
            item = QListWidgetItem(self)
            self.addItem(item)
            row = ComponentListItem(part[0], part[1]) # component class and count
            self.items.append(row)
            item.setSizeHint(row.minimumSizeHint())
            self.setItemWidget(item, row)

class ComponentListItem(QWidget):
    def __init__(self, part, count, *args, **kw):
        super().__init__(*args, **kw)

        self.row = QGridLayout()

        self.part_id = part.id
        self.part_name = part.name
        self.name_label = QLabel(part.name)

        self.count_label = QLabel(str(count))
        self.plus_button = QPushButton("+")
        self.plus_button.setFixedWidth(30)
        self.minus_button = QPushButton("-")
        self.minus_button.setFixedWidth(30)
        count_layout = QHBoxLayout()
        count_layout.addWidget(self.minus_button)
        count_layout.addWidget(self.count_label)
        count_layout.addWidget(self.plus_button)

        self.row.addWidget(self.name_label, 0, 0, 1, 1, alignment=Qt.AlignLeft)
        self.row.addLayout(count_layout, 0, 1, 1, 1, alignment=Qt.AlignRight)
        
        self.setContentsMargins(0, 0, 0, 0)
        # self.row.addWidget(self.plus_button, 0, 1, 1, 1, alignment=Qt.AlignRight)
        # self.row.addWidget(self.count_label, 0, 2, 1, 1, alignment=Qt.AlignRight)
        # self.row.addWidget(self.minus_button, 0, 3, 1, 1, alignment=Qt.AlignRight)

        self.setLayout(self.row)

class BoxesList(QListWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.items = []
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
    
    def clear_items(self):
        self.clear()
        self.items = []

    def populate(self, boxes):
        for box in boxes:
            item = QListWidgetItem(self)
            self.addItem(item)
            row = BoxesListItem(box)
            self.items.append(row)
            item.setSizeHint(row.minimumSizeHint())
            self.setItemWidget(item, row)

        # item = QListWidgetItem(self)
        # self.addItem(item)
        # item.setSizeHint(self.add_box_button.minimumSizeHint())
        # self.setItemWidget(item, self.add_box_button)

class BoxesListItem(QWidget):
    def __init__(self, box, *args, **kw):
        super().__init__(*args, **kw)

        self.row = QGridLayout()

        self.box_id = box.id
        self.name_label = QLabel(box.name)

        self.row.addWidget(self.name_label, 0, 0, 1, 1, alignment=Qt.AlignLeft)

        self.setLayout(self.row)
        self.setContentsMargins(0, 0, 0, 0)


class TopBar(QWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

class BottomBar(QWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.setContentsMargins(0, 0, 0, 0)
        layout = QHBoxLayout()
        layout.setSpacing(25)
        self.savedIndicator = QLabel("Saved")
        layout.addWidget(self.savedIndicator)
        self.job_label = QLabel("Current Job: ...")
        layout.addWidget(self.job_label)
        self.progressBar = QProgressBar()
        layout.addWidget(self.progressBar)
        self.setLayout(layout)

class NavBarGroups(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []

    def clear_items(self):
        self.clear()
        self.items = []

    def populate(self, items):
        self.items = items
        for item in items:
            self.addItem(NavBarGroupItem(item.id, item.name))
        self.sortItems()

    def set_selected_item_id(self, id):
        for i in range(self.count()):
            if self.item(i).id == id:
                self.setCurrentItem(self.item(i))
                break

class NavBarBoxes(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []

    def clear_items(self):
        self.clear()
        self.items = []

    def populate(self, items):
        self.items = items
        for item in items:
            self.addItem(NavBarBoxItem(item.id, item.name))
        self.sortItems()

    def set_selected_item_id(self, id):
        for i in range(self.count()):
            if self.item(i).id == id:
                self.setCurrentItem(self.item(i))
                break
        
class NavBarGroupItem(QListWidgetItem):
    def __init__(self, id, name, *args, **kwargs):
        super().__init__(name)
        self.id = id
        self.name = name

class NavBarBoxItem(QListWidgetItem):
    def __init__(self, id, name, *args, **kwargs):
        super().__init__(name)
        self.id = id
        self.name = name