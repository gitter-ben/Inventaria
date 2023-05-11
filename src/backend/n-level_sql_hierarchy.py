import sqlite3
from sqlite3 import Error

class NLevelSQLHierarchy:
    def __init__(self, db_file, hierarchy_level=1):
        '''Initialize a new SQLite Hierarchy

        :param: db_file: The path to the database file. If none exists, a new one will be made.
        :param: hierarchy_level: The number of groups (folders) the hierarchy has, 0 will be only parts
        '''

        self.conn = self._create_connection(db_file)
        self.cursor = self.conn.cursor()

        self._initialize_hierarchy(hierarchy_level)

    def _initialize_hierarchy(self, hl):
        '''Initialize the hierarchy and create tables for all of the levels

        :param: hl: the number of groups and subgroups
        '''
        with self.conn:
            if hl == 0:
                sql_create_parts = """CREATE TABLE IF NOT EXISTS parts (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                );"""
                self.cursor.execute(sql_create_parts)

            else:
                sql_create_toplevel = """CREATE TABLE IF NOT EXISTS level1 (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    is_part BOOLEAN DEFAULT FALSE
                );"""
                self.cursor.execute(sql_create_toplevel)

                sql_create_parts = f"""CREATE TABLE IF NOT EXISTS parts (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    parent_id BIGINT,
                    FOREIGN KEY (parent_id)
                        REFERENCES level{hl} (parent_id)
                );"""
                self.cursor.execute(sql_create_parts)

                for level in range(hl, 1, -1):
                    print(f"Making level{level}")
                    sql_create_level = f"""CREATE TABLE IF NOT EXISTS level{level} (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        parent_id BIGINT,
                        FOREIGN KEY (parent_id)
                            REFERENCES level{level-1} (parent_id)
                    );"""
                    self.cursor.execute(sql_create_level)

    def _create_connection(self, db_file):
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(f"Could not connect to database:\n{e}")
            return e
        
        return conn

    def get_level(self, level):
        with self.conn:
            rows = self.cursor.execute(f"SELECT name, is_part FROM level{level}")
        return rows.fetchall()

    def get_all_parts(self):
        rows = self.cursor.execute("SELECT name FROM parts")
        return rows.fetchall()

    def print_tree(self):
        print("Top-level:")
        rows = self.cursor.execute("SELECT id, name, is_part FROM level1").fetchall()
        for row in rows:
            if row[2] == 1:
                print(f"- {row[1]} (Part)")
            elif row[2] == 0:
                print(f"- {row[1]} (Dir)")
                self._print_tree_helper(2, row[0])

    def _print_tree_helper(self, level, id, indent=1):
        

if __name__ == "__main__":
    h = NLevelSQLHierarchy("database.sqlite", hierarchy_level=2)

    h.print_tree()