from PyQt6.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import sys

from constants import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APPLICATION_NAME)

        self.button_states = {"button1": False}
        
        self.button = QPushButton("HELLO MF")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.the_button_was_toggled)
        self.button.setChecked(self.button_states["button1"])

        #self.setMinimumSize(x, y)
        self.setFixedSize(800, 600)
        #self.setMaximumSize(x, y)

        self.setCentralWidget(self.button)

    def the_button_was_toggled(self, state):
        self.button_states["button1"] = state
        print(f"Current state: {self.button_states['button1']}")

        self.button.setText("Already clicked me.")
        self.button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()