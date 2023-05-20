"""!
@file database.py
@brief Defines the database for the "parts" inventory type.
"""
import sqlite3

from core.utils import DBConnectError
from core.database_abstract import DBBaseClass
from .signal_master import PartsSignalMaster


class PartsDatabase(DBBaseClass):
    def __init__(self, db_file: str, sig_master: PartsSignalMaster):
        self.conn = None
        self.cur = None
        self.saved = None

        self._signal_master = sig_master
        self.load_from_file(db_file)

    def load_from_file(self, db_file) -> None:
        """!
        @brief Load a database from an .sqlite file.
        """
        self.conn = self._create_connection(db_file)
        self.cur = self.conn.cursor()
        self._initialize_database()

        self.saved = True
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
        self.saved = True
        self.make_savepoint()
        self._signal_master.save_state_changed.emit(True)

    def rollback_to_savepoint(self) -> None:
        """!
        @brief rollback to last savepoint by executing ROLLBACK TRANSACTION;
        """
        self.cur.execute("ROLLBACK TRANSACTION;")
        self.saved = True
        self.make_savepoint()
        self._signal_master.save_state_changed.emit(True)

    def save(self) -> None:
        """!
        @brief Save the database by committing the current transaction.
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

    @staticmethod
    def _create_connection(self, file_name: str) -> sqlite3.Connection:
        try:
            conn = sqlite3.connect(file_name, isolation_level=None)
        except sqlite3.Error:
            raise DBConnectError

        return conn
