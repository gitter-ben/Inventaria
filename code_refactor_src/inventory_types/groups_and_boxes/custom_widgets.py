"""!
@file custom_widgets.py
@brief Contains all of the custom widgets 
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout

from groups_and_boxes_signal_master import GroupsAndBoxesSignalMaster


signal_master = GroupsAndBoxesSignalMaster()

class Editor(QWidget):
    def __init__(self, *args, **kw):
        super(Editor, self).__init__(*args, **kw)

        self.button = QPushButton("Press me")
        self.button.clicked.connect(lambda: self.signal_master.editor_button_pressed.emit("a string"))

        layout = QHBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
