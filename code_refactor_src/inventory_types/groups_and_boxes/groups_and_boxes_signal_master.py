"""!
@file groups_and_boxes_signal_master.py
"""

from PyQt5.QtCore import pyqtSignal, QObject


class GroupsAndBoxesSignalMaster(QObject):
    """!
    @brief The signal master for the groups and boxes inventory type.
    """
    # Editor signals
    group_name_changed = pyqtSignal(int, str)
    box_name_changed = pyqtSignal(int, str)

    group_description_changed = pyqtSignal(int, str)
    box_description_changed = pyqtSignal(int, str)

    delete_group = pyqtSignal(int)
    delete_box = pyqtSignal(int)

    add_box = pyqtSignal(int)
    add_box_content = pyqtSignal(int)

    set_box_content_count = pyqtSignal(int, int)

    # NavBar signals
    new_group = pyqtSignal()
    new_box = pyqtSignal()

    navbar_group_selection_changed = pyqtSignal()
    navbar_box_selection_changed = pyqtSignal()

    # Database signals
    save_state_changed = pyqtSignal(bool)

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
