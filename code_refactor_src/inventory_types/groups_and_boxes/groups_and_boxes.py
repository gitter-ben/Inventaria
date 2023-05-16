"""!
@file groups_and_boxes.py
@brief Defines the inspector for the groups and boxes inventory type

@section todo_groups_and_boxes TODO
- Reimplement everything but with doxygen comments and cleaned up
- Implement PyQt QTests with automatic GUI testing
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.Qt import QPalette, QColor, pyqtSlot

from .custom_widgets import GroupsAndBoxesEditor#, NavBars
from .groups_and_boxes_signal_master import GroupsAndBoxesSignalMaster

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
        self.editor = GroupsAndBoxesEditor()
        
        class TestGroup:
            id = 9
            name = "hello mf"
            description = "A cool description"

        self.editor.set_group_info(TestGroup())
        
        self.signal_master.group_name_changed.connect(self.name_changed_slot)
        self.signal_master.box_name_changed.connect(self.name_changed_slot)
        
        self.signal_master.group_description_changed.connect(self.group_description_changed_slot)
        self.signal_master.box_description_changed.connect(self.box_description_changed_slot)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.editor)
        self.setLayout(self.layout)


    @pyqtSlot(int, str)
    def name_changed_slot(self, id, name):
        print(f"(ID: {id}) changed name to '{name}'")


    @pyqtSlot(int, str)
    def group_description_changed_slot(self, id, new_description):
        print(f"Group (ID: {id}) changed its description to {new_description}")


    @pyqtSlot(int, str)
    def box_description_changed_slot(self, id, new_description):
        print(f"Box (ID: {id}) changed its description to {new_description}")

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
