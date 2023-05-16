from enum import Enum

class GroupsAndBoxesEditorMode(Enum):
    """!
    @brief An enum to describe the state the GroupsAndBoxEditor is in right now
    """
    GROUP = 1
    BOX = 2
    EMPTY = 3