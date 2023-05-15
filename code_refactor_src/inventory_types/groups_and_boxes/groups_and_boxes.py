"""!
@file groups_and_boxes.py
@brief Defines the inspector for the groups and boxes inventory type

@section todo_groups_and_boxes TODO
- Reimplement everything but with doxygen comments and cleaned up
- Implement PyQt QTests with automatic GUI testing
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import QPalette, QColor

class GroupsAndBoxes(QWidget):
    def __init__(self, x: int, *args, **kw) -> GroupsAndBoxes:
        """!
        Initializes a new inspector for the groups and boxes inventory type.
        Steps:
        1. Initializes the QWidget superclass
        2. Calls the setup_gui function to setup the GUI
        

        @return  A new GroupsAndBoxes object
        """

        super(GroupsAndBoxes, self).__init__(*args, **kw)
        self.setup_GUI()


    def setup_GUI(self):
        """!
        Sets up the entire GUI for the groups and boxes inspector.
        Steps:
        1. Setup colors and stylesheets
        2. 

        """

        # ========== Setup colors and stylesheets==============
        # Set the QSplitter handles to a gray
        self.setStyleSheet("QSplitter::handle { background-color: #AAAAAA }")
        
        # Set background color to (200, 200, 200)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(200, 200, 200))
        self.setPalette(palette)
        # =====================================================

        # ========== 
