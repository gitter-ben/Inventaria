"""!
@file database.py
@brief Includes the MainDatabase class for the application.
"""
import json
import os
from pprint import pprint

from PyQt5.Qt import pyqtSlot, QObject

from core.signal_master import MainSignalMaster
from core.utils import MainDBLoadError
from inventory_types.groups_and_boxes import (
    GroupsAndBoxesGUI,
    GroupsAndBoxesDatabase,
    GroupsAndBoxesSignalMaster
)

db_types = {
    "groups and boxes": (
        GroupsAndBoxesGUI,
        GroupsAndBoxesDatabase,
        GroupsAndBoxesSignalMaster
    )
}


class MainDatabase(QObject):
    """!
    @brief The main database class for Inventaria.

    Database directory layout:
    - config.json: Includes the config for the database, contains list of sub-databases and filenames.
    - databases: Includes all sub-databases
      - <id>_<inventory_type>.sqlite: Name format for sub-databases
      - ...
    - parts.sqlite: The database for all shared parts.
    """
    def __init__(self, dir_name: str, sig_master: MainSignalMaster, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._signal_master = sig_master
        self.saved = True
        self._db_loaded = False
        self._sub_databases = []
        self._config = None
        self.load_database(dir_name)

    def save(self) -> None:
        if self.saved:  # No action required
            return

        for db in self._sub_databases:
            db[1].save()

        self.saved = True
        self._signal_master.main_save_state_changed.emit(True)
        print("Database saved.")

    def un_save(self) -> None:
        self.saved = False
        self._signal_master.main_save_state_changed.emit(False)

    def roll_back(self) -> None:
        self.saved = True
        self._signal_master.main_save_state_changed.emit(True)
        print("Database rolled back.")

    def load_database(self, dir_path: str) -> None:
        """!
        @brief Load a database from a directory.
        """
        try:
            with open(os.path.join(dir_path, "config.json")) as f:
                self._config = json.load(f)
                print(f"New database. Config: {self._config}")
        except FileNotFoundError:
            raise MainDBLoadError("No config.json file found.")

        for db in self._config["databases"]:
            sig_master = db_types[db["type"]][2]()
            sub_db = db_types[db["type"]][1](os.path.join(dir_path, db["file"]), sig_master)
            gui = db_types[db["type"]][0](sub_db, sig_master, self._signal_master)
            sig_master.save_state_changed.connect(self._sub_db_save_state_changed)
            self._sub_databases.append((gui, sub_db, sig_master))
            self._signal_master.new_inventory_tab.emit(gui, db["file"])

        pprint(self._sub_databases)

    def new(self, path) -> None:
        pass

    def close(self) -> None:
        if self._db_loaded:
            for sub in self._sub_databases:
                sub.close()
        print("Database closed.")

    @pyqtSlot(bool)
    def _sub_db_save_state_changed(self, saved: bool) -> None:
        if saved:  # No action required
            return

        self.saved = False
