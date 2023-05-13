from top_level_boxes_hierarchy import *
from PyQt5 import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from constants import *
import sys
import resources
from custom_widgets import *

class Inspector(QWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        super_layout = QGridLayout()

        self.headline = QLabel("Inspector")
        font = self.headline.font()
        font.setPointSize(13)
        self.headline.setFont(font)
        self.description = QPlainTextEdit()
        
        self.buttoncontainer = QWidget()
        button_layout = QGridLayout()
        button_layout.setAlignment(Qt.AlignRight)
        ic = QIcon(":/icons/delete_icon.png")
        self.delete_button = QPushButton("Delete")
        self.delete_button.setIcon(ic)
        button_layout.addWidget(self.delete_button, 0, 0, 1, 1)
        self.buttoncontainer.setLayout(button_layout)

        self.components_list = ComponentsList()
        self.components_list.addItem(QListWidgetItem("hello"))

        #layout.addWidget(self.headline, 0, 0, 1, 1

        super_layout.setAlignment(Qt.AlignTop)
        super_layout.addWidget(self.headline, 0, 0, 1, 1)
        super_layout.addWidget(self.description, 1, 0, 1, 2)
        super_layout.addWidget(self.components_list, 2, 0, 1, 2)
        super_layout.addWidget(self.buttoncontainer, 3, 0, 1, 2)
        self.setLayout(super_layout)

    def empty(self):
        self.headline.setText("Inspector: No box/group selected")
        self.description.clear()

    def setGroupInfo(self, group: Group):
        self.headline.setText(f"Group Inspector: {group.name} ({group.id})")
        self.description.setPlainText(group.description)

    def setBoxInfo(self, box: Box):
        self.headline.setText(f"Box Inspector: {box.name} ({box.id})")
        self.description.setPlainText(box.description)

class ComponentsList(QListWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
    
    def populate(self, parts):
        pass

class ComponentListItem(QWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

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