"""!
@file database.py
@brief Defines the database for the "parts" inventory type.
"""
import sqlite3

from invtype_bases import DatabaseBase
from core.utils import DBConnectError
from .common import Part
from .signal_master import PartsSignalMaster


class PartsDatabase(DatabaseBase):
    def __init__(self, db_file: str, sig_master: PartsSignalMaster):
        super().__init__(sig_master)
        self.conn = None
        self.cur = None

        self.load_from_file(db_file)

    def load_from_file(self, db_file) -> None:
        """!
        @brief Load a database from an .sqlite file.
        """
        self.conn = self._create_connection(db_file)
        self.cur = self.conn.cursor()
        self._initialize_database()

        self._saved = True
        self.make_savepoint()

    def close(self) -> None:
        """!
        @brief Gracefully close the connection to a database file.
        """
        self.conn.close()

    def make_savepoint(self) -> None:
        """!
        @brief Create a savepoint by starting an sqlite transaction.
        """
        self.cur.execute("ROLLBACK TRANSACTION;")
        self._saved = True
        self.make_savepoint()

    def rollback_to_savepoint(self) -> None:
        """!
        @brief rollback to last savepoint by executing ROLLBACK TRANSACTION;
        """
        self.cur.execute("ROLLBACK TRANSACTION;")
        self._saved = True
        self.make_savepoint()

    def save(self) -> None:
        """!
        @brief Save the database by committing the current transaction.
        """
        if not self._saved:
            self.cur.execute("COMMIT TRANSACTION;")
            self._saved = True
            self.make_savepoint()

    def get_parts(self):
        parts = [Part(*row) for row in self.cur.execute(
            "SELECT id, name FROM parts"
        )]
        return parts

    def get_part(self, part_id):
        part = Part(*self.cur.execute(
            "SELECT id, name FROM parts WHERE id=?",
            (part_id, )
        ))
        return part

    @DatabaseBase.changes_db
    def add_part(self, name):
        self.cur.execute(
            "INSERT INTO parts (name) VALUES (?);",
            (name, )
        )

    def _unsaved(self) -> None:
        if self._saved:
            self._saved = False

    def _initialize_database(self):
        sql_foreign_keys_on = """PRAGMA FOREIGN_KEYS = ON"""

        sql_create_parts_table = """CREATE TABLE IF NOT EXISTS parts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );"""

        with self.conn:
            self.cur.execute(sql_foreign_keys_on)
            self.cur.execute(sql_create_parts_table)

    @staticmethod
    def _create_connection(file_name: str) -> sqlite3.Connection:
        try:
            conn = sqlite3.connect(file_name, isolation_level=None)
        except sqlite3.Error:
            raise DBConnectError

        return conn
