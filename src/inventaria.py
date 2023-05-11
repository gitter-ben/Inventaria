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

        for i in range(2):
            layout = QListWidget()
            layout.setMinimumWidth(WINDOW_WIDTH//6)
            
            for line in [f"Sample text {i}" for i in range(1, 100)]:
                layout.addItem(QListWidgetItem(line))

            self.sideBar.addWidget(layout)

        self.setCentralWidget(self.GUIVSplitter)

    def refreshSidebars(self):
        pass


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()