"""!
@file database.py
@brief The file containing all the database stuff for the groups and boxes inventory type
"""
import sqlite3
from typing import List

from core.utils import DBConnectError  # , changes_db
from core.database_abstract import DBBaseClass
from inventory_types.parts import PartsDatabase
from .common import Group, Box, BoxContentItem
from .signal_master import GroupsAndBoxesSignalMaster


class GroupsAndBoxesDatabase(DBBaseClass):
    """!
    @brief Database class for the groups and boxes inventory type.
    """
    def __init__(self, db_file: str, sig_master: GroupsAndBoxesSignalMaster, parts_db: PartsDatabase):
        """!
        @brief Initialize a new GroupsAndBoxesDatabase.

        @return A new GroupsAndBoxesDatabase instance
        """
        self.conn = None
        self.cur = None
        self.saved = None

        self._signal_master = sig_master
        self._parts_db = parts_db
        self.load_from_file(db_file)

    def load_from_file(self, db_file) -> None:
        """!
        @brief Load a new database from a .sqlite file.
        """
        self.conn = self._create_connection(db_file)
        self.cur = self.conn.cursor()
        self._initialize_database()

        self.saved = True
        self.make_savepoint()

    def close(self) -> None:
        """!
        @brief Gracefully close the connection ta a database.
        """
        self.conn.close()

    def make_savepoint(self) -> None:
        """!
        @brief Create a savepoint by starting a sqlite transaction.
        """
        self.cur.execute("BEGIN TRANSACTION;")

    def rollback_to_savepoint(self) -> None:
        """!
        @brief Rollback to last savepoint by executing "ROLLBACK TRANSACTION;" in sqlite
        """
        self.cur.execute("ROLLBACK TRANSACTION;")
        self.saved = True
        self.make_savepoint()
        self._signal_master.save_state_changed.emit(True)

    def save(self) -> None:
        """!
        @brief Save the database to the file.
        Save the current database by committing the current transaction
        and starting a new one by calling self.make_savepoint()
        """
        if not self.saved:
            self.cur.execute("COMMIT TRANSACTION;")
            self.saved = True
            self.make_savepoint()
            self._signal_master.save_state_changed.emit(True)

    def _unsaved(self) -> None:
        if self.saved:
            self.saved = False
            self._signal_master.save_state_changed.emit(False)

    def get_groups(self) -> List[Group]:
        """!
        Get all groups as Group instances

        @return A list of instances of the Group dataclass
        """
        groups = [Group(*row) for row in self.cur.execute(
            "SELECT id, name, description FROM groups"
        ).fetchall()]
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
            "SELECT id, group_id, name, description FROM boxes WHERE group_id=?",
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
            "SELECT id, group_id, name, description FROM boxes WHERE id=?",
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
            """SELECT a.id, a.box_id, b.name, a.count FROM box_contents AS a 
            JOIN parts AS b ON b.id = a.part_id 
            WHERE a.box_id = ?""",
            (box_id, )
        ).fetchall()]

        return contents

    @DBBaseClass.changes_db
    def add_group(self, name: str) -> None:
        """!
        Add a new group with a name.

        @param name: The name of the new group.
        """
        self.cur.execute(
            "INSERT INTO groups (name) VALUES (?)",
            (name,)
        )

    @DBBaseClass.changes_db
    def delete_group(self, group_id: int) -> None:
        """!
        Delete a group via the group id.

        @param group_id: The id of the group to delete
        """
        self.cur.execute(
            "DELETE FROM groups WHERE id=?",
            (group_id, )
        )

    @DBBaseClass.changes_db
    def edit_group_name(self, group_id: int, name: str) -> None:
        """!
        Edit a group name via a group id and a new name.

        @param group_id: The id of the group to edit.
        @param name: The new name of the group.
        """
        self.cur.execute(
            "UPDATE groups SET name=? WHERE id=?",
            (name, group_id)
        )

    @DBBaseClass.changes_db
    def edit_group_description(self, group_id: int, description: str) -> None:
        """!
        Edit a group description via a group id and a new description
        """
        self.cur.execute(
            "UPDATE groups SET description=? WHERE id=?",
            (description, group_id)
        )

    @DBBaseClass.changes_db
    def add_box(self, name: str, group_id: int) -> None:
        """!
        Add a new box with a set name and a group id.

        @param name: The name of the new box.
        @param group_id: The group id of the new box.
        """
        self.cur.execute(
            "INSERT INTO boxes (name, group_id) VALUES (?, ?)",
            (name, group_id)
        )

    @DBBaseClass.changes_db
    def delete_box(self, box_id: int) -> None:
        """!
        Delete a box with a set box id. The cascading mode will also remove all parts associated with the box.

        @param box_id: The id of the box to delete.
        """
        self.cur.execute(
            "DELETE FROM boxes WHERE id=?",
            (box_id, )
        )

    @DBBaseClass.changes_db
    def edit_box_name(self, box_id: int, new_name: str) -> None:
        """!
        Edit the name of a box with a set box id and a new name.

        @param box_id: The id of the box to edit.
        @param new_name: The new name of the box.
        """
        self.cur.execute(
            "UPDATE boxes SET name=? WHERE id=?",
            (new_name, box_id)
        )

    @DBBaseClass.changes_db
    def edit_box_description(self, box_id: int, description: str) -> None:
        """!
        Edit the description of a box with a box id and new description.

        @param box_id: The id of the box to edit.
        @param description: The new description of the box.
        """
        self.cur.execute(
            "UPDATE boxes SET description=? WHERE id=?",
            (description, box_id)
        )

    @DBBaseClass.changes_db
    def add_box_contents(self, box_id: int, part_id: int, count: int) -> None:
        """!
        Add a new box_contents to a box via a box_id and a part_id.

        @param box_id: The id of the box to add to.
        @param part_id: The id of the part to add to it.
        @param count: The number of parts to add.
        """
        self.cur.execute(
            "INSERT INTO box_contents (box_id, count, part_id) VALUES (?, ?, ?);",
            (box_id, count, part_id)
        )

    @DBBaseClass.changes_db
    def edit_box_contents_count(self, box_contents_id: int, count: int) -> None:
        """!
        Edit the count of an item in a box contents via the box contents id and the count.

        @param box_contents_id: The id of the box contents.
        @param count: The new count.
        """
        self.cur.execute(
            "UPDATE box_contents SET count=? WHERE id=?",
            (count, box_contents_id)
        )

    def _initialize_database(self) -> None:
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
            description TEXT
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
    def _create_connection(db_file) -> sqlite3.Connection:
        """!
        Create a connection to a database file. Raises the custom DBConnectError in case of an error during connection.

        @param db_file: The filepath to the database.

        @return An instance of the sqlite3.Connection class
        """
        try:
            conn = sqlite3.connect(db_file, isolation_level=None)
        except sqlite3.Error:
            raise DBConnectError

        return conn
