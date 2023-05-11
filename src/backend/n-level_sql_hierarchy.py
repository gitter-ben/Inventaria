import sqlite3
from sqlite3 import Error

class NLevelSQLHierarchy:
    def __init__(self, db_file, hierarchy_level=1):
        '''Initialize a new SQLite Hierarchy

        :param: db_file: The path to the database file. If none exists, a new one will be made.
        :param: hierarchy_level: The number of groups (folders) the hierarchy has, 0 will be only parts
        '''

        self.conn = self._create_connection(db_file)
        self.cursor = self.conn.cursor

        self._initialize_hierarchy(hierarchy_level)

    def _initialize_hierarchy(self, hl):
        if hl == 0:
            sql_create_parts = """CREATE TABLE IF NOT EXISTS (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );"""
        else:
            sql_create_parts = f"""CREATE TABLE IF NOT EXISTS (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                parent_id BIGINT,
                FOREIGN KEY (parent_id)
                    REFERENCES level{hl} (parent_id)
            );"""
        
            sql_create_sublevels = []
            for level in range(hl, 1, -1):
                sql_create_sublevels.append(f"""CREATE TABLE IF NOT EXISTS (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    parent_id BIGINT,
                    FOREIGN KEY (parent_id)
                        REFERENCES level{level} (parent_id)
                );""")

            sql_create_toplevel = """CREATE TABLE IF NOT EXISTS (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );"""

            with self.conn:
                self.cursor


    def _create_connection(self, db_file):
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(f"Could not connect to database:\n{e}")
            return e
        
        return conn