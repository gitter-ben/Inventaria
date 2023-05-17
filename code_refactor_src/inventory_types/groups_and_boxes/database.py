"""!
@file database.py
@brief The file containing all the database stuff for the groups and boxes inventory type
"""
from functools import wraps
from typing import List

import sqlite3

from code_refactor_src.core.utils import DBConnectError
from code_refactor_src.inventory_types.groups_and_boxes.common import Group, Box, BoxContentItem


class GroupsAndBoxesDatabase:
    def __init__(self):
        """!
        Initialize a new GroupsAndBoxesDatabase.

        @return A new GroupsAndBoxesDatabase instance
        """
        self.conn = None
        self.cur = None

    def load_from_file(self, db_file):
        """!
        Load a new database from a .sqlite file.
        """
        self.conn = self._create_connection(db_file)
        self.cur = self.conn.cursor()
        self._initialize_database()

    def close(self):
        """!
        Gracefully close the connection ta a database.
        """
        self.conn.close()

    def get_groups(self) -> List[Group]:
        """!
        Get all groups as Group instances

        @return A list of instances of the Group dataclass
        """
        groups = [Group(*row) for row in self.cur.execute(
            "SELECT id, name, description FROM groups").fetchall()]
        return groups

    def get_group(self, group_id: int) -> Group:
        """!
        Get a group via its group_id.

        @param group_id The id of the group to look up.

        @return An instance of the Group dataclass
        """
        group = Group(*self.cur.execute(
            "SELECT id, name, description FROM groups WHERE id=?",
            (group_id, )
        ).fetchone())

        return group

    def get_boxes(self, group_id: int) -> List[Box]:
        """!
        Get a list of all boxes in a group via group_id.

        @param group_id: The group_id of the boxes to look up

        @return A list of instances of the Box dataclass
        """
        boxes = [Box(*row) for row in self.cur.execute(
            "SELECT id, name, description FROM boxes WHERE group_id=?",
            (group_id, )
        ).fetchall()]

        return boxes

    def get_box(self, box_id: int) -> Box:
        """!
        Get a box by its box_id. Group_id not needed due to box_ids being unique.

        @param box_id: The id of the box to look up.

        @return An instance of the Box dataclass.
        """
        box = Box(*self.cur.execute(
            "SELECT id, name, description FROM boxes WHERE id=?",
            (box_id, )
        ).fetchone())

        return box

    def get_box_contents(self, box_id: int) -> List[BoxContentItem]:
        """!
        Get the contents of a box by the box_id.

        @param box_id: The id of the box to look up.

        @return A list of instances of the BoxContentItem dataclass.
        """
        contents = [BoxContentItem(*row) for row in self.cur.execute(
            """SELECT a.id, b.name, a.count FROM box_contents AS a \
            JOIN parts AS b ON b.id = a.part_id \
            WHERE a.box_id = ? \
            """,
            (box_id, )
        ).fetchall()]

        return contents

    def _initialize_database(self):
        """!
        Initialize the database by creating all necessary tables if they don't exist. Also enable foreign keys.
        """
        sql_foreign_keys_on = """PRAGMA FOREIGN_KEYS = ON"""

        sql_create_parts_table = """CREATE TABLE IF NOT EXISTS parts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );"""

        sql_create_groups_table = """CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL
        );"""

        sql_create_boxes_table = """CREATE TABLE IF NOT EXISTS boxes (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            group_id INTEGER NOT NULL,
            FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE CASCADE
        );"""

        sql_create_box_contents_table = """CREATE TABLE IF NOT EXISTS box_contents (
            id INTEGER PRIMARY KEY,
            count INT NOT NULL,
            box_id INTEGER NOT NULL,
            part_id INTEGER NOT NULL,
            FOREIGN KEY (box_id) REFERENCES boxes (id) ON DELETE CASCADE,
            FOREIGN KEY (part_id) REFERENCES parts (id) ON DELETE CASCADE
        );"""

        with self.conn:
            self.cur.execute(sql_foreign_keys_on)
            self.cur.execute(sql_create_parts_table)
            self.cur.execute(sql_create_groups_table)
            self.cur.execute(sql_create_boxes_table)
            self.cur.execute(sql_create_box_contents_table)

    @staticmethod
    def _changes_db(func):
        """!
        A decorator to describe a function that changes the database.
        Calls the self.unsaved() method to send the saveStateChanged to the editor that it is now not saved anymore.
        """
        @wraps(func)
        def wrapper(self, *args, **kw):
            self.unsaved()
            return func(self, *args, **kw)
        return wrapper

    @staticmethod
    def _create_connection(db_file) -> sqlite3.Connection:
        """!
        Create a connection to a database file. Raises the custom DBConnectError in case of an error during connection.

        @param db_file: The filepath to the database.

        @return An instance of the sqlite3.Connection class
        """
        try:
            conn = sqlite3.connect(db_file, isolation_level=None)
        except sqlite3.Error as e:
            print(f"Could not connect to database:\n{e}")
            raise DBConnectError

        return conn
