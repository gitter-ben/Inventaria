from dataclasses import dataclass
from enum import Enum
from typing import Optional, NamedTuple


class GroupAndBoxIDs(NamedTuple):
    """!
    @brief Presents a pair of ids for current group and box.
    """
    group_id: Optional[int]
    box_id: Optional[int]

    def __repr__(self):
        return f"<GroupAndBoxIDS: group_id={self.group_id}, box_id={self.box_id}>"


class GroupsAndBoxesEditorMode(Enum):
    """!
    @brief An enum to describe the state the GroupsAndBoxEditor is in right now
    """
    GROUP = 1
    BOX = 2
    EMPTY = 3


@dataclass
class BoxContentItem:
    """!
    @brief Dataclass for a box content item.

    Fields:
    - id: int
    - box_id: int
    - name: str
    - count: positive int
    """
    id: int
    box_id: int
    name: str
    count: int


@dataclass
class Box:
    """!
    @brief Dataclass for a box.

    Fields:
    - id: int
    - group_id: int
    - name: str
    - description: str
    """
    id: int
    group_id: int
    name: str
    description: str


@dataclass
class Group:
    """!
    @brief Dataclass for a group.

    Fields:
    - id: int
    - name: str
    - description: str
    """
    id: int
    name: str
    description: str
