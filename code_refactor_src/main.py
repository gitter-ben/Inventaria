"""!
@file main.py
@brief The main file with the entry point for the program.

"""

import sys

from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import QMainWindow

from inventory_types.groups_and_boxes import *


def main():
    """! The main entry point of Inventaria"""
    app = QApplication(sys.argv)
    window = QMainWindow()
    db = GroupsAndBoxesDatabase("groups_and_boxes.sqlite")
    thing = GroupsAndBoxes(db)
    window.setCentralWidget(thing)
    window.show()

    thing._editor.set_group_info(db.get_group(1), db.get_boxes(1))

    app.exec()


if __name__ == "__main__":
    main()
