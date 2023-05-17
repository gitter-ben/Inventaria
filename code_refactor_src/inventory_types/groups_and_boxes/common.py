from enum import Enum
from dataclasses import dataclass
from typing import List


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
    name: str
    count: int


@dataclass
class Box:
    id: int
    name: str
    description: str


@dataclass
class Group:
    id: int
    name: str
    description: str
