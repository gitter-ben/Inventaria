"""!
@file groups_and_boxes.py
@brief Defines the inspector for the groups and boxes inventory type

@section todo_groups_and_boxes TODO
- Reimplement everything but with doxygen comments and cleaned up
- Implement PyQt QTests with automatic GUI testing
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.Qt import QPalette, QColor, pyqtSlot

from custom_widgets import Editor#, NavBars
from groups_and_boxes_signal_master import GroupsAndBoxesSignalMaster

class GroupsAndBoxes(QWidget):
    def __init__(self, *args, **kw):
        """!
        Initializes a new inspector for the groups and boxes inventory type.
        Steps:
        1. Initializes the QWidget superclass
        2. Acquire a Singleton instance of the GroupsAndBoxesSignalMaster class
        3. Calls the setup_gui function to setup the GUI
        

        @return  A new GroupsAndBoxes object
        """

        super(GroupsAndBoxes, self).__init__(*args, **kw) # Initialize QWidget superclass

        self.signal_master = GroupsAndBoxesSignalMaster() # Acquire singleton instance of signal master
        
        self.setup_GUI() # Setup the GUI


    def setup_GUI(self):
        """!
        Sets up the entire GUI for the groups and boxes inspector.
        Steps:
        1. Setup colors and stylesheets
        2. Setup editor and signals


        @return  None
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

        # ========== Setup editor =============================
        # Instantiate a new editor and connect signals
        self.editor = Editor()
        self.signal_master.editor_button_pressed.connect(self.button_pressed_slot)
        self.editor.show()


    @pyqtSlot(str)
    def button_pressed_slot(self, thing):
        print(f"Smth else and {thing}")


def test():
    from PyQt5.Qt import QApplication
    from PyQt5.QtWidgets import QMainWindow
    import sys

    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setCentralWidget(main_widget := GroupsAndBoxes())
    window.show()

    app.exec()

if __name__ == "__main__":
    test()
