"""!
@file main.py
@brief The main file with the entry point for the program.

"""

import sys

from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import QMainWindow

from code_refactor_src.ui_main import MainWindow


def main():
    """! The main entry point of Inventaria"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
