import sqlite3
from sqlite3 import Error
import os

class Hierarchy:

    def __init__(self, sqlite_file):

        self.conn = self.create_connection(sqlite_file)
        self.c = self.conn.cursor()
        self.setup_db()
        self.add_box("Superclamps", "Rigging")
        self.add_box("VGA Kabel", "Video")
        self.add_component("VGA Kabel 2m", "Video")
        self.add_component("Superclamp", "Rigging", box_name="Superclamps")
    
        self.close()

    def create_connection(self, db_file):
        '''Create a connection to an SQLite Database
           specified by a sqlite database file
        
        :param: db_file: database file
        :return: Connection object or None
        '''
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)

        return conn

    def setup_db(self):
        sql_create_component_table = """CREATE TABLE IF NOT EXISTS components (
            component_id integer PRIMARY KEY,
            component_name text NOT NULL,
            box_id INTEGER NULLABLE,
            group_id INTEGER NOT NULL,
            FOREIGN KEY (group_id)
                REFERENCES groups (group_id),
            FOREIGN KEY (box_id)
                REFERENCES boxes (box_id)
        );"""

        sql_create_boxes_table = """CREATE TABLE IF NOT EXISTS boxes (
            box_id integer PRIMARY KEY, 
            box_name text NOT NULL UNIQUE,
            group_id INTEGER,
            FOREIGN KEY (group_id)
                REFERENCES groups (group_id)
        );"""

        sql_create_groups = """CREATE TABLE IF NOT EXISTS groups (
            id integer PRIMARY KEY,
            name text NOT NULL
        );"""

        sql_make_groups = """INSERT INTO groups (name) VALUES ('Licht'), ('Audio'), ('Allgemein'), ('Rigging'), ('Sonstige'), ('Video');"""

        with self.conn:
            self.c.execute(sql_create_groups)
            self.c.execute(sql_make_groups)
            self.c.execute(sql_create_boxes_table)
            self.c.execute(sql_create_component_table)

    def add_box(self, name, group):
        '''Create a new box with a name and a parent group

        :param: name: The name of the box
        :param: group: The name of the topgroup
        '''

        with self.conn:
            self.c.execute("INSERT INTO boxes (box_name, group_id) VALUES (?, (SELECT id FROM groups WHERE name=?))", (name, group))

    def add_component(self, name, group, box_name=None):
        '''Create a new component with a name and an optional box

        :param: name: The name of the component
        :param: group: The name of the group the component is in
        :param: box_name: The name of the box it's in,  default=None
        '''
        
        if box_name:
            with self.conn:
                self.c.execute("INSERT INTO components (component_name, box_id, group_id) VALUES (?, (SELECT box_id FROM boxes WHERE box_name=?), (SELECT id FROM groups WHERE name=?))", (name, box_name, group))
        else:
            with self.conn:
                self.c.execute("INSERT INTO components (component_name, box_id, group_id) VALUES (?, NULL, (SELECT id FROM groups WHERE name=?))", (name, group))

    def close(self):
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    hierarchy = Hierarchy("database.sqlite")
    hierarchy.close()
