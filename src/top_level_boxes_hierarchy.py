import sqlite3
from utils import *

class Group:
    def __init__(self, id, name):
        self.name = name
        self.id = id

class Box:
    def __init__(self, id, name):
        self.name = name
        self.id = id


class Database:
    def __init__(self, db_file):
        self.conn = self._create_connection(db_file)
        
        if self.conn is None:
            raise DBConnectError()

        self.cur  = self.conn.cursor()
        self.initialize_db()
    
    def initialize_db(self):
        sql_create_parts_table = """CREATE TABLE IF NOT EXISTS parts (
            id INTEGER PRIMARY KEY,
            name TEXT,
            box_id INTEGER,
            FOREIGN KEY (box_id) REFERENCES boxes (id) ON DELETE CASCADE
        );"""

        sql_create_boxes_table = """CREATE TABLE IF NOT EXISTS boxes (
            id INTEGER PRIMARY KEY,
            name TEXT,
            group_id INTEGER,
            FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE CASCADE,
            UNIQUE(name, group_id)
        )"""

        sql_create_groups_table = """CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE 
        );"""

        with self.conn:
            self.cur.execute(sql_create_groups_table)
            self.cur.execute(sql_create_boxes_table)
            self.cur.execute(sql_create_parts_table)
    
    def get_group_names(self):
        with self.conn:
            rows = list(map(lambda x: x[0], self.cur.execute("SELECT name FROM groups").fetchall()))
        return rows
    
    def get_groups(self):
        with self.conn:
            groups = [Group(row[0], row[1]) for row in self.cur.execute("SELECT * FROM groups").fetchall()]
        return groups

    def add_group(self, name):
        if name in self.get_group_names():
            print("Error: that group exists!")
            return -1

        with self.conn:
            self.cur.execute("INSERT INTO ")

    def get_group_info(self, group_name):
        with self.conn:
            rows = self.cur.execute("SELECT * FROM groups WHERE name=?", (group_name, )).fetchall()
        return rows

    # def set_group_info(self, group_name, data):
    #     pass

    def get_box_names(self, group_id):
        with self.conn:
            rows = list(map(lambda x: x[0], self.cur.execute("SELECT name FROM boxes WHERE group_id=?", (group_name, )).fetchall()))
        return rows

    def get_boxes(self, group_id):
        with self.conn:
            boxes = [Box(row[0], row[1]) for row in self.cur.execute("SELECT * FROM boxes WHERE group_id=?", (group_id, )).fetchall()]
        return boxes

    def get_box_info(self, group_id, box_id):
        with self.conn:
            rows = self.cur.execute("SELECT * FROM boxes WHERE id=? AND group_id=?", (box_id, group_id)).fetchall()

    def get_box_contents(self, group_name, box_name):
        with self.conn:
            rows = self.cur.execute("SELECT * FROM parts WHERE box_id=(SELECT id FROM boxes WHERE name=? AND group_id=(SELECT id FROM groups WHERE name=?))", (box_name, group_name)).fetchall()

    def _create_connection(self, db_file):
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(f"Could not connect to database:\n{e}")

        return conn

if __name__ == "__main__":
    db = Database("database.sqlite")