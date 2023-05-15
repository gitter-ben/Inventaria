"""!
@file groups_and_boxes_signal_master.py
"""

from PyQt5.QtCore import pyqtSignal, QObject
from utils import Singleton


class GroupsAndBoxesSignalMaster(QObject, metaclass=Singleton):
    editor_button_pressed = pyqtSignal(str)

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
