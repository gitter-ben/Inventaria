import sqlite3
from utils import *
from PyQt5.QtCore import pyqtSignal, QObject
from functools import wraps

class Group:
    def __init__(self, id, name, description):
        self.name = name
        self.id = id
        self.description = description

class Box:
    def __init__(self, id, name, description):
        self.name = name
        self.id = id
        self.description = description

class Database(QObject):
    saveStateChanged = pyqtSignal(bool)

    def __init__(self, db_file):
        super().__init__()

        self.conn = self._create_connection(db_file)
        
        if self.conn is None:
            raise DBConnectError()

        self.cur  = self.conn.cursor()
        self.initialize_db()

        self.saved = True
        self.make_savepoint()


    def unsaved(self):
        if self.saved:
            self.saveStateChanged.emit(False)
            self.saved = False

    def make_savepoint(self):
        self.cur.execute("BEGIN TRANSACTION;")

    def rollback_to_savepoint(self):
        self.cur.execute("ROLLBACK TRANSACTION;")

    def save(self):
        if not self.saved:
            self.cur.execute("COMMIT TRANSACTION;")
            self.saved = True
            self.saveStateChanged.emit(True)
            self.make_savepoint()

    def changesDB(func):
        @wraps(func)
        def wrapper(self, *args, **kw):
            self.unsaved()
            return func(self, *args, **kw)
        return wrapper


    def initialize_db(self):
        sql_create_parts_table = """CREATE TABLE IF NOT EXISTS parts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            box_id INTEGER,
            FOREIGN KEY (box_id) REFERENCES boxes (id) ON DELETE CASCADE
        );"""

        sql_create_boxes_table = """CREATE TABLE IF NOT EXISTS boxes (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description VARCHAR(200),
            group_id INTEGER,
            FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE CASCADE
        );"""

        sql_create_groups_table = """CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description VARCHAR(200)
        );"""

        with self.conn:
            self.cur.execute(sql_create_groups_table)
            self.cur.execute(sql_create_boxes_table)
            self.cur.execute(sql_create_parts_table)
    
    def get_group_names(self):
        rows = list(map(lambda x: x[0], self.cur.execute("SELECT name FROM groups").fetchall()))
        return rows
    
    def get_groups(self):
        groups = [Group(*row) for row in self.cur.execute("SELECT id, name, description FROM groups").fetchall()]
        return groups

    def get_group_info(self, group_id):
        group = Group(*self.cur.execute("SELECT id, name, description FROM groups WHERE id=?", (group_id, )).fetchone())
        return group

    def get_box_names(self, group_id):
        rows = list(map(lambda x: x[0], self.cur.execute("SELECT name FROM boxes WHERE group_id=?", (group_id, )).fetchall()))
        return rows

    def get_boxes(self, group_id):
        boxes = [Box(*row) for row in self.cur.execute("SELECT id, name, description FROM boxes WHERE group_id=?", (group_id, )).fetchall()]
        return boxes

    def get_box_info(self, group_id, box_id):
        box = Box(*self.cur.execute("SELECT id, name, description FROM boxes WHERE id=? AND group_id=?", (box_id, group_id)).fetchone())
        return box



    @changesDB
    def add_group(self, name):
        self.cur.execute("INSERT INTO groups (name) VALUES (?);", (name, ))

    @changesDB
    def add_box(self, group_id, name):
        self.cur.execute("INSERT INTO boxes (name, group_id) VALUES (?, ?);", (name, group_id))
        self.unsaved()


    def _create_connection(self, db_file):
        try:
            conn = sqlite3.connect(db_file, isolation_level=None)
        except Error as e:
            print(f"Could not connect to database:\n{e}")

        return conn

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = Database("database.sqlite")