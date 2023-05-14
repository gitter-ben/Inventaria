from backend.python_json_approach import *
from PyQt5 import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from constants import *
import sys

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.db = Hierarchy()
        # self.db.add_sublevel("Audio")
        # self.db.add_sublevel("Video")
        # self.db.add_sublevel("Licht")
        # self.db.add_sublevel("Rigging")
        # self.db.add_sublevel("Allgemein")
        # self.db.add_sublevel("Sonstiges")

        # self.db.add_things(Things("Stromkabel 30m 16A", 3))
        # self.db.add_sublevel_to_path(["Video"], "VGA Kabel Box")
        # self.db.add_things_to_path(["Video", "VGA Kabel Box"], Things("VGA Kabel 3m", 10))
        # self.db.add_things_to_path(["Video", "VGA Kabel Box"], Things("VGA Kabel 5m", 5))
        # self.db.add_things_to_path(["Video", "VGA Kabel Box"], Things("VGA Kabel 1m", 13))

        # self.selected_path = []
        # self.navigation_bars = []

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
        self.inspector = QWidget()
        self.inspector.setMinimumWidth(WINDOW_WIDTH//4)
        #self.inspector_button = QPushButton(self.inspector)
        #self.inspector_button.pressed.connect(self.refreshSidebars)

        self.sideBar = QSplitter(Qt.Horizontal)
        self.GUIHSplitter = QSplitter(Qt.Horizontal)
        self.GUIHSplitter.addWidget(self.sideBar)
        self.GUIHSplitter.addWidget(self.inspector)
        self.GUIHSplitter.setCollapsible(0, False) # Can't collapse "Filemanager"
        self.GUIHSplitter.setCollapsible(1, False) # Can't collapse Inspector
        self.topBar = QWidget()
        self.topBar.setMinimumHeight(WINDOW_HEIGHT//8)
        self.GUIVSplitter = QSplitter(Qt.Vertical)
        self.GUIVSplitter.addWidget(self.topBar)
        self.GUIVSplitter.addWidget(self.GUIHSplitter)
        self.GUIVSplitter.setSizes([WINDOW_HEIGHT//7, WINDOW_HEIGHT//7 * 6])
        self.GUIVSplitter.setCollapsible(0, False)
        self.setCentralWidget(self.GUIVSplitter)

        self.sideBar.addWidget(self.new_navigation_bar(self.db.get_sublevel_names_from_path([]), self.db.get_things_names_from_path([]), self.path_selection_changed))

#     def new_navigation_bar(self, sublevels, data, change_func):
#         qlist = NavigationBar(sublevels, data, change_func)
#         self.navigation_bars.append(qlist)
#         self.sideBar.addWidget(qlist)
#         return qlist

#     def path_selection_changed(self, text):
#         path = []
#         for nav in self.navigation_bars:
#             try:
#                 path.append(nav.sublevel_list.currentItem().text())
#             except AttributeError:
#                 break
#             print('ello')
#             nav.deleteLater()

# class NavigationBar(QWidget):
#     def __init__(self, sublevels, things, changed_func, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.sublevels = sublevels
#         self.things = things
#         self.changed_func = changed_func

#         self.setContentsMargins(0, 0, 0, 0)

#         layout = QVBoxLayout()
#         self.sublevel_label = QLabel()
#         self.sublevel_label.setText("Sublevels")
#         layout.addWidget(self.sublevel_label)
#         self.sublevel_list = QListWidget(self)
#         self.sublevel_list.addItems(self.sublevels)#[QListWidgetItem(line) for line in self.sublevels])
#         self.sublevel_list.currentTextChanged.connect(self.changed_func)
#         layout.addWidget(self.sublevel_list)

#         self.things_label = QLabel("Things")
#         layout.addWidget(self.things_label)
#         self.things_list = QListWidget(self)
#         self.things_list.addItems(self.things)#[QListWidgetItem(self.things_list, line) for line in self.things])
#         layout.addWidget(self.things_list)

#         self.setLayout(layout)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()