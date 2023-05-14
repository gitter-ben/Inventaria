from top_level_boxes_hierarchy import *
from PyQt5 import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from constants import *
import sys
import resources
from custom_widgets import *

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db = None
        self.db_loaded = False
        self.setupGUI()

        self.GUIHSplitter.setEnabled(False)

    def load_db(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/', "Sqlite Databases (*.sqlite)")[0]
        if fname is None or len(fname) == 0:
            return

        if self.db_loaded:
            self.unload_db()
        
        self.db = Database(fname)
        self.db.saveStateChanged.connect(self.saveStateChangedSlot)

        self.group_level_nav.populate(self.db.get_groups())
        self.groupSelectionChanged()
        self.db_loaded = True
        self.GUIHSplitter.setEnabled(True)

    def unload_db(self):
        if not self.db_loaded:
            self.showMessage("Error", "No database to unload")
            return
        
        if not self.db.saved:
            reply = QMessageBox.question(self, "Close without saving", "Are you sure you want to unload this database without saving?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return

        self.group_level_nav.clearSelection()
        self.group_level_nav.clear_items()
        self.box_level_nav.clearSelection()
        self.box_level_nav.clear_items()
        self.GUIHSplitter.setEnabled(False)
        self.db.close()
        self.db_loaded = False
        del self.db
    
    def setupGUI(self):
        self.statusBar()

        self.setWindowTitle(APPLICATION_NAME)
        #self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet("QSplitter::handle { background-color: #AAAAAA; }")
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(200, 200, 200))
        self.setPalette(palette)

        # Make top menubar
        self.openAction = QAction("&Open", self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.setStatusTip("Open a file")
        self.openAction.triggered.connect(self.load_db)
        
        self.saveAction = QAction("&Save", self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.setStatusTip("Save the current database")
        self.saveAction.triggered.connect(self.saveSlot)

        self.unloadAction = QAction("&Unload", self)
        self.unloadAction.setStatusTip("Unload the current database")
        self.unloadAction.triggered.connect(self.unload_db)

        self.quitAction = QAction("&Quit", self)
        self.quitAction.setShortcut("Ctrl+Q")
        self.quitAction.setStatusTip("Quit the application")
        self.quitAction.triggered.connect(self.close)

        self.preferencesAction = QAction("&Preferences")
        self.preferencesAction.setShortcut("Ctrl+P")
        self.preferencesAction.setStatusTip("Show the preferences")
        self.preferencesAction.triggered.connect(self.showPreferences)

        self.aboutAction = QAction("&About", self)
        self.aboutAction.setStatusTip("Show the about section")
        self.aboutAction.triggered.connect(self.showAbout)

        self.toolBar = self.menuBar()
        fileMenu = self.toolBar.addMenu("&File")
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.unloadAction)
        fileMenu.insertSeparator(self.quitAction)
        fileMenu.addAction(self.quitAction)
        editMenu = self.toolBar.addMenu("&Edit")
        editMenu.addAction(self.preferencesAction)
        toolsMenu = self.toolBar.addMenu("&Tools")
        helpMenu = self.toolBar.addMenu("&Help")
        helpMenu.addAction(self.aboutAction)

        # Make inspector and sidebar layout
        self.inspector = Inspector()
        self.inspector.setMinimumWidth(WINDOW_WIDTH//2)
        self.inspector.descriptionChanged.connect(self.inspectorDescriptionChanged)
        self.inspector.deleteBox.connect(self.inspectorDeleteBox)
        self.inspector.deleteGroup.connect(self.inspectorDeleteGroup)

        self.navBars = QSplitter(Qt.Horizontal)
        self.GUIHSplitter = QSplitter(Qt.Horizontal)
        self.GUIHSplitter.addWidget(self.navBars)
        self.GUIHSplitter.addWidget(self.inspector)
        self.GUIHSplitter.setSizes([WINDOW_HEIGHT//3, 2 * WINDOW_HEIGHT//3])
        self.GUIHSplitter.setCollapsible(0, False) # Can't collapse Navigator
        self.GUIHSplitter.setCollapsible(1, False) # Can't collapse Inspector
        self.topBar = TopBar()
        self.topBar.setFixedHeight(TOP_BAR_HEIGHT)
        self.bottomBar = BottomBar()
        self.bottomBar.setFixedHeight(BOTTOM_BAR_HEIGHT)
        self.GUIVSplitter = QSplitter(Qt.Vertical)
        self.GUIVSplitter.addWidget(self.topBar)
        self.GUIVSplitter.addWidget(self.GUIHSplitter)
        self.GUIVSplitter.addWidget(self.bottomBar)
        #self.GUIVSplitter.setSizes([40, WINDOW_HEIGHT//7 * 6, BOTTOM_BAR_HEIGHT])
        self.GUIVSplitter.setCollapsible(0, False)
        self.GUIVSplitter.setCollapsible(1, False)
        self.GUIVSplitter.setCollapsible(2, False)
        self.setCentralWidget(self.GUIVSplitter)

        # Setup top bar
        layout = QGridLayout()
        ic = QIcon(":/icons/open_file_icon.png")
        self.loadButton = QPushButton("Load")
        self.loadButton.setFixedWidth(65)
        self.loadButton.setIcon(ic)
        self.loadButton.pressed.connect(self.load_db)
        layout.addWidget(self.loadButton, 0, 0, 1, 1)
        ic = QIcon(":/icons/save_icon.png")
        self.saveButton = QPushButton("Save")
        self.saveButton.setFixedWidth(65)
        self.saveButton.setIcon(ic)
        layout.addWidget(self.saveButton, 0, 1, 1, 1)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.topBar.setLayout(layout)
        
        self.saveButton.pressed.connect(self.saveSlot)

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
        # self.group_level_nav.populate(self.db.get_groups())
        self.group_level_nav.setSortingEnabled(True)
        self.group_level_nav.sortItems()
        self.group_level_nav.currentRowChanged.connect(self.groupSelectionChanged)
        layout.addWidget(label := QLabel("Groups"), 0, 0, 1, 1)
        font = label.font()
        font.setPointSize(13)
        label.setFont(font)
        self.new_group_button = QPushButton("")
        self.new_group_button.clicked.connect(self.newGroupSlot)
        ic = QIcon(":/icons/green_plus.png")
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
        ic = QIcon(":/icons/green_plus.png")
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

        self.saveStateChangedSlot(True)

    def inspectorDeleteGroup(self, group_id):
        print(f"Delete group with id: {str(group_id)}")
        if self.db_loaded:
            self.db.delete_group(group_id)
            self.group_level_nav.clearSelection()
            self.group_level_nav.clear_items()
            self.group_level_nav.populate(self.db.get_groups())
    
    def inspectorDeleteBox(self, box_id):
        if self.db_loaded:
            self.db.delete_box(self.group_level_nav.currentItem().id, box_id)
            self.box_level_nav.clearSelection()
            self.box_level_nav.clear_items()
            self.box_level_nav.populate(self.db.get_boxes(self.group_level_nav.currentItem().id))
            #self.groupSelectionChanged()
            #self.boxSelectionChanged()

    def inspectorDescriptionChanged(self, group_box_or_empty, text):
        if self.db_loaded:
            print(f"You changed the {'group' if group_box_or_empty == GROUP else ('box' if group_box_or_empty == BOX else 'empty')} description to: \n{text}")
            if group_box_or_empty == GROUP:
                self.db.edit_group_description(self.group_level_nav.currentItem().id, text)
            elif group_box_or_empty == BOX:
                self.db.edit_box_description(self.group_level_nav.currentItem().id, self.box_level_nav.currentItem().id, text)

    def showPreferences(self):
        print("Show the preferences")

    def showAbout(self):
        print("Show the about")

    def closeEvent(self, event):
        if self.db_loaded:
            if not self.db.saved:
                reply = QMessageBox.question(self, "Close without saving", "Are you sure you want to close without saving?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                if reply == QMessageBox.Yes:
                    self.db.close()
                    event.accept()
                else:
                    event.ignore()
            else:
                self.db.close()
                event.accept()

    def saveSlot(self):
        if self.db_loaded:
            if not self.db.saved:
                self.db.save()
        else:
            self.showMessage("Error", "No database to save")

    def saveStateChangedSlot(self, saved):
        if saved:
            self.saveButton.setEnabled(False)
            self.bottomBar.savedIndicator.setText("Saved")
        else:
            self.saveButton.setEnabled(True)
            self.bottomBar.savedIndicator.setText("Not Saved")

    def newGroupSlot(self):
        name, ok = QInputDialog.getText(self, "New Group", "Name:  ")
        if ok:
            if len(name) == 0:
                self.showMessage("Error", "Name must be at least one letter!")
            else:
                self.db.add_group(name)
                self.group_level_nav.clearSelection()
                self.group_level_nav.clear_items()
                self.group_level_nav.populate(self.db.get_groups())

    def newBoxSlot(self):
        if self.group_level_nav.currentItem() is None:
            self.showMessage("Error", "No group is selected!")
            return
        name, ok = QInputDialog.getText(self, "New Box", "Name:  ")
        if ok:
            if len(name) == 0:
                self.showMessage("Error", "Name must be at least one letter!")
            else:
                self.db.add_box(self.group_level_nav.currentItem().id, name)
                self.box_level_nav.clear_items()
                self.box_level_nav.populate(self.db.get_boxes(self.group_level_nav.currentItem().id))
                self.groupSelectionChanged()
                self.boxSelectionChanged()

    def showMessage(self, title: str, msg: str):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(msg)
        dlg.show()

    def boxSelectionChanged(self):
        selected_box = self.box_level_nav.currentItem()
        selected_group = self.group_level_nav.currentItem()
        if selected_box and selected_group:
            self.inspector.setBoxInfo(self.db.get_box_info(selected_group.id, selected_box.id))
        self.group_level_nav.sortItems()

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

        self.group_level_nav.sortItems()
        self.box_level_nav.sortItems()

