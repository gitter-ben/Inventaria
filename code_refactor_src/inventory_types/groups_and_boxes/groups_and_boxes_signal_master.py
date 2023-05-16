"""!
@file groups_and_boxes_signal_master.py
"""

from PyQt5.QtCore import pyqtSignal, QObject

from core.utils import Singleton
from .common import GroupsAndBoxesEditorMode

class GroupsAndBoxesSignalMaster(QObject, metaclass=Singleton):
    
    # Editor signals
    group_name_changed = pyqtSignal(int, str)
    box_name_changed = pyqtSignal(int, str)

    group_description_changed = pyqtSignal(int, str)
    box_description_changed = pyqtSignal(int, str)

    add_box = pyqtSignal()
    add_component = pyqtSignal()

    # Database signals
    save_state_changed = pyqtSignal(bool)


    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
