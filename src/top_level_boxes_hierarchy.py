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

class Component:
    def __init__(self, id, name):
        self.id = id
        self.name = name

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
        self.saved = True
        self.make_savepoint()
        self.saveStateChanged.emit(True)

    def save(self):
        if not self.saved:
            self.cur.execute("COMMIT TRANSACTION;")
            self.saved = True
            self.make_savepoint()
            self.saveStateChanged.emit(True)

    def changesDB(func):
        @wraps(func)
        def wrapper(self, *args, **kw):
            self.unsaved()
            return func(self, *args, **kw)
        return wrapper


    def initialize_db(self):
        sql_create_parts_table = """CREATE TABLE IF NOT EXISTS parts (
            id INTEGER PRIMARY KEY,
            count INT NOT NULL,    
            box_id INTEGER NOT NULL,
            template_id INTEGER NOT NULL,
            FOREIGN KEY (box_id) REFERENCES boxes (id) ON DELETE CASCADE,
            FOREIGN KEY (template_id) REFERENCES part_templates (id) ON DELETE CASCADE
        );"""

        # template_id INTEGER NOT NULL,
        # FOREIGN KEY (template_id) REFERENCES part_templates (id) ON DELETE CASCADE,

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

        sql_create_part_templates_table = """CREATE TABLE IF NOT EXISTS part_templates (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );"""

        sql_foreign_keys_on = "PRAGMA FOREIGN_KEYS = ON"

        with self.conn:
            self.cur.execute(sql_foreign_keys_on)
            self.cur.execute(sql_create_groups_table)
            self.cur.execute(sql_create_boxes_table)
            self.cur.execute(sql_create_part_templates_table)
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

    def get_box_contents(self, group_id, box_id):
        rows = self.cur.execute("SELECT id, count, template_id FROM parts WHERE box_id=? AND (SELECT group_id FROM boxes WHERE box_id=?)=?", (box_id, box_id, group_id)).fetchall()
        components = []
        for row in rows:
            name = self.cur.execute("SELECT name FROM part_templates WHERE id=?", (row[2], )).fetchone()[0]
            components.append((Component(row[0], name), row[1]))

        return components

    
    @changesDB
    def edit_component_count(self, part_id, count_diff):
        self.cur.execute("UPDATE parts SET count=count+? WHERE id=?", (count_diff, part_id))

    @changesDB
    def add_group(self, name):
        self.cur.execute("INSERT INTO groups (name) VALUES (?);", (name, ))

    @changesDB
    def delete_group(self, group_id):
        self.cur.execute("DELETE FROM groups WHERE id=?", (group_id, ))

    @changesDB
    def edit_group_description(self, group_id, new_description):
        self.cur.execute("UPDATE groups SET description=? WHERE id=?", (new_description, group_id))

    @changesDB
    def edit_group_name(self, group_id, new_name):
        self.cur.execute("UPDATE groups SET name=? WHERE id=?", (new_name, group_id))

    @changesDB
    def add_box(self, group_id, name):
        self.cur.execute("INSERT INTO boxes (name, group_id) VALUES (?, ?);", (name, group_id))

    @changesDB
    def delete_box(self, group_id, box_id):
        self.cur.execute("DELETE FROM boxes WHERE group_id=? AND id=?", (group_id, box_id))

    @changesDB
    def edit_box_description(self, group_id, box_id, new_description):
        self.cur.execute("UPDATE boxes SET description=? WHERE id=? AND group_id=?", (new_description, box_id, group_id))

    @changesDB
    def edit_box_name(self, group_id, box_id, new_name):
        self.cur.execute("UPDATE boxes SET name=? WHERE id=? AND group_id=?", (new_name, box_id, group_id))

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
    db.get_box_contents(2, 3)