"""!
@file database.py
@brief The file containing all the database stuff for the groups and boxes inventory type
"""

import sqlite3

from code_refactor_src.core.utils import DBConnectError


class GroupsAndBoxesDatabase:
    def __init__(self):
        self.conn = None

    def load_from_file(self, db_file):
        self.conn = self.create_connection(db_file)
        self._initialize_database()

    def close(self):
        self.conn.close()

    def _initialize_database(self):
        pass

    @staticmethod
    def create_connection(db_file):
        try:
            conn = sqlite3.connect(db_file, isolation_level=None)
        except sqlite3.Error as e:
            print(f"Could not connect to database:\n{e}")
            raise DBConnectError

        return conn
