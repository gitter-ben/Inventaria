from enum import Enum
from dataclasses import dataclass


class GroupsAndBoxesEditorMode(Enum):
    """!
    @brief An enum to describe the state the GroupsAndBoxEditor is in right now
    """
    GROUP = 1
    BOX = 2
    EMPTY = 3


@dataclass
class BoxContentItem:
    id: int
    box_id: int
    name: str
    count: int


@dataclass
class Box:
    id: int
    group_id: int
    name: str
    description: str


@dataclass
class Group:
    id: int
    name: str
    description: str
