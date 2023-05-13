from top_level_boxes_hierarchy import *
from PyQt5 import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from constants import *
import sys

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db = Database("database.sqlite")

        self.setupGUI()
    
    def setupGUI(self):
        self.setWindowTitle(APPLICATION_NAME)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet("QSplitter::handle { background-color: #AAAAAA; }")
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(200, 200, 200))
        self.setPalette(palette)

        # Make top menubar
        self.toolBar = self.menuBar()
        fileMenu = self.toolBar.addMenu("&File")
        fileMenu = self.toolBar.addMenu("&Edit")
        fileMenu = self.toolBar.addMenu("&Tools")
        fileMenu = self.toolBar.addMenu("&About")

        # Make inspector and sidebar layout
        self.inspector = Inspector()
        self.inspector.setMinimumWidth(WINDOW_WIDTH//2)
        self.navBars = QSplitter(Qt.Horizontal)
        self.GUIHSplitter = QSplitter(Qt.Horizontal)
        self.GUIHSplitter.addWidget(self.navBars)
        self.GUIHSplitter.addWidget(self.inspector)
        self.GUIHSplitter.setSizes([WINDOW_HEIGHT//3, 2 * WINDOW_HEIGHT//3])
        self.GUIHSplitter.setCollapsible(0, False) # Can't collapse Navigator
        self.GUIHSplitter.setCollapsible(1, False) # Can't collapse Inspector
        self.topBar = TopBar()
        self.topBar.setMinimumHeight(WINDOW_HEIGHT//8)
        self.bottomBar = BottomBar()
        self.bottomBar.setFixedHeight(BOTTOM_BAR_HEIGHT)
        self.GUIVSplitter = QSplitter(Qt.Vertical)
        self.GUIVSplitter.addWidget(self.topBar)
        self.GUIVSplitter.addWidget(self.GUIHSplitter)
        self.GUIVSplitter.addWidget(self.bottomBar)
        self.GUIVSplitter.setSizes([WINDOW_HEIGHT//7, WINDOW_HEIGHT//7 * 6, BOTTOM_BAR_HEIGHT])
        self.GUIVSplitter.setCollapsible(0, False)
        self.GUIVSplitter.setCollapsible(1, False)
        self.GUIVSplitter.setCollapsible(2, False)
        self.setCentralWidget(self.GUIVSplitter)


        # Make group level navbar:
        #    __________________
        #   |  Label |  Button |
        #   |------------------|
        #   |    Item 1        |
        #   |__________________|
        #   |    Item 2        |
        #   |__________________|
        #   |    Item 3        |
        #   |__________________|
        #

        self.group_level_nav_container = QWidget()
        layout = QGridLayout()
        self.group_level_nav = NavBarGroups()
        self.group_level_nav.populate(self.db.get_groups())
        self.group_level_nav.currentRowChanged.connect(self.groupSelectionChanged)
        layout.addWidget(label := QLabel("Groups"), 0, 0, 1, 1)
        font = label.font()
        font.setPointSize(13)
        label.setFont(font)
        ic = QIcon("../icons/green_plus.png")
        self.new_group_button = QPushButton("")
        self.new_group_button.clicked.connect(self.newGroupSlot)
        self.new_group_button.setIcon(ic)
        layout.addWidget(self.new_group_button, 0, 1, 1, 1)
        self.new_group_button = QPushButton("New Group")
        self.new_group_button.clicked.connect(self.newGroupSlot)
        layout.addWidget(self.group_level_nav, 1, 0, 1, 2)
        self.group_level_nav_container.setLayout(layout)
        self.navBars.addWidget(self.group_level_nav_container)

        # Make box level navbar (same layout see above)

        self.box_level_nav_container = QWidget()
        layout = QGridLayout()
        self.box_level_nav = NavBarBoxes()
        layout.addWidget(label := QLabel("Boxes"), 0, 0, 1, 1)
        font = label.font()
        font.setPointSize(13)
        label.setFont(font)
        ic = QIcon("../icons/green_plus.png")
        self.new_box_button = QPushButton("")
        self.new_box_button.clicked.connect(self.newBoxSlot)
        self.new_box_button.setIcon(ic)
        layout.addWidget(self.new_box_button, 0, 1, 1, 1)
        layout.addWidget(self.box_level_nav, 1, 0, 1, 2)
        self.box_level_nav.currentRowChanged.connect(self.boxSelectionChanged)
        self.box_level_nav_container.setLayout(layout)
        self.navBars.addWidget(self.box_level_nav_container)

        self.navBars.setChildrenCollapsible(False)
        self.inspector.empty()

    def newGroupSlot(self):
        pass

    def newBoxSlot(self):
        pass

    def boxSelectionChanged(self):
        selected_box = self.box_level_nav.currentItem()
        selected_group = self.group_level_nav.currentItem()
        if selected_box and selected_group:
            self.inspector.setBoxInfo(self.db.get_box_info(selected_group.id, selected_box.id))

    def groupSelectionChanged(self):
        selected_group = self.group_level_nav.currentItem()
        if selected_group:
            self.box_level_nav.clear_items()
            self.box_level_nav.populate(self.db.get_boxes(selected_group.id))
            self.inspector.setGroupInfo(self.db.get_group_info(selected_group.id))
        else:
            self.inspector.empty()
            self.box_level_nav.clear_items()
            self.group_level_nav.clear_items()
            self.group_level_nav.populate(self.db.get_groups())


class Inspector(QWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        layout = QGridLayout()
        container = QWidget(self)
        self.headline = QLabel("Inspector")
        font = self.headline.font()
        font.setPointSize(13)
        self.headline.setFont(font)
        self.description = QPlainTextEdit()

        #self.image = QLabel(self)
        #self.imagemap = QPixmap("image.jpeg")
        #self.image.setPixmap(self.imagemap)

        layout.addWidget(self.headline, 0, 0, 1, 1)
        #layout.addWidget(self.image, 1, 0, alignment=Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(self.description, 1, 0, 1, 1)
        container.setLayout(layout)
        #self.setCentralWidget(container)

    def empty(self):
        self.headline.setText("Inspector: No box/group selected")

    def setGroupInfo(self, group: Group):
        self.headline.setText(f"Group Inspector: {group.name} ({group.id})")
        self.description.setPlainText(group.description)
        self.description.setVisible(True)
        #self.image.setVisible(True)

    def setBoxInfo(self, box: Box):
        self.headline.setText(f"Box Inspector: {box.name} ({box.id})")
        self.description.setPlainText(box.description)
        self.description.setVisible(True)
        #self.image.setVisible(True)


class TopBar(QWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

class BottomBar(QWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.setContentsMargins(0, 0, 0, 0)
        layout = QHBoxLayout()
        layout.setSpacing(25)
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

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()