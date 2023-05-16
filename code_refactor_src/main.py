"""!
@file main.py
@brief The main file with the entry point for the program.

"""

import sys

from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import QMainWindow

from inventory_types.groups_and_boxes.groups_and_boxes import GroupsAndBoxes

def main():
    """! The main entry point of Inventaria"""
    app = QApplication(sys.argv)
    window = QMainWindow()
    thing = GroupsAndBoxes()
    window.setCentralWidget(thing)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()