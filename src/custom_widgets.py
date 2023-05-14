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
    deleteBox = pyqtSignal(int)
    deleteGroup = pyqtSignal(int)

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        super_layout = QGridLayout()

        self.headline = QLabel("Inspector")
        font = self.headline.font()
        font.setPointSize(13)
        self.headline.setFont(font)

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
        self.boxes_list = BoxesList()
        #self.boxes_list.populate(["Hello mf", "hello mf 2", "hello there"])

        self.components_label = QLabel("Components: ")
        font = self.components_label.font()
        font.setPointSize(11)
        self.components_label.setFont(font)
        self.components_list = ComponentsList()
        #self.components_list.populate(["Hello mf", "hello mf 2", "hello there"])

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
        super_layout.addWidget(self.description_label, 1, 0, 1, 1)
        super_layout.addWidget(self.description, 2, 0, 1, 2)
        
        super_layout.addWidget(self.components_label, 3, 0, 1, 1)
        super_layout.addWidget(self.components_list, 4, 0, 1, 2)

        super_layout.addWidget(self.boxes_label, 5, 0, 1, 1)
        super_layout.addWidget(self.boxes_list, 6, 0, 1, 2)
        
        super_layout.addWidget(self.buttoncontainer, 7, 0, 1, 2)

        self.setLayout(super_layout)
        self.empty()

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
        self.group_box_or_empty = EMPTY

    def setGroupInfo(self, group: Group):
        self.group = group
        self.box = None

        self.headline.setText(f"Group Inspector: {group.name} ({group.id})")

        self.description.blockSignals(True)
        self.description.setPlainText(group.description)
        self.description.blockSignals(False)
        
        self.boxes_list.clear_items()
        self.boxes_list.populate(["Test box 1, test box 2", "test box 3"])
        self.components_label.setVisible(False)
        self.components_list.setVisible(False)
        self.boxes_label.setVisible(True)
        self.boxes_list.setVisible(True)
        self.description_label.setVisible(True)
        self.description.setVisible(True)
        self.buttoncontainer.setVisible(True)
        self.group_box_or_empty = GROUP

    def setBoxInfo(self, box: Box):
        self.box = box
        self.group = None

        self.headline.setText(f"Box Inspector: {box.name} ({box.id})")

        self.description.blockSignals(True)
        self.description.setPlainText(box.description)
        self.description.blockSignals(False)
        
        self.components_list.clear_items()
        self.components_list.populate(["Test component 1", "test 2", "test 3"])
        self.boxes_label.setVisible(False)
        self.boxes_list.setVisible(False)
        self.components_label.setVisible(True)
        self.components_list.setVisible(True)
        self.description_label.setVisible(True)
        self.description.setVisible(True)
        self.buttoncontainer.setVisible(True)
        self.group_box_or_empty = BOX

class ComponentsList(QListWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.items = []
    
    def clear_items(self):
        self.clear()
        self.items = []

    def populate(self, parts):
        for part in parts:
            item = QListWidgetItem(self)
            self.addItem(item)
            row = ComponentListItem(part, 300)
            self.items.append(row)
            item.setSizeHint(row.minimumSizeHint())
            self.setItemWidget(item, row)

class ComponentListItem(QWidget):
    def __init__(self, name, count, *args, **kw):
        super().__init__(*args, **kw)

        self.row = QGridLayout()

        self.name_label = QLabel(name)
        self.count_label = QLabel(str(count))

        self.row.addWidget(self.name_label, 0, 0, 1, 1, alignment=Qt.AlignLeft)
        self.row.addWidget(self.count_label, 0, 1, 1, 1, alignment=Qt.AlignRight)

        self.setLayout(self.row)

class BoxesList(QListWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.items = []
    
    def clear_items(self):
        self.clear()
        self.items = []

    def populate(self, parts):
        for part in parts:
            item = QListWidgetItem(self)
            self.addItem(item)
            row = BoxesListItem(part, 300)
            self.items.append(row)
            item.setSizeHint(row.minimumSizeHint())
            self.setItemWidget(item, row)

class BoxesListItem(QWidget):
    def __init__(self, name, count, *args, **kw):
        super().__init__(*args, **kw)

        self.row = QGridLayout()

        self.name_label = QLabel(name)
        self.count_label = QLabel(str(count))

        self.row.addWidget(self.name_label, 0, 0, 1, 1, alignment=Qt.AlignLeft)
        self.row.addWidget(self.count_label, 0, 1, 1, 1, alignment=Qt.AlignRight)

        self.setLayout(self.row)


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