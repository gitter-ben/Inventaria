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
from inventory_types.parts import PartsGUI, PartsDatabase, PartsSignalMaster

db_types = {
    "groups and boxes": (
        GroupsAndBoxesGUI,
        GroupsAndBoxesDatabase,
        GroupsAndBoxesSignalMaster
    ),
    "parts": (
        PartsGUI,
        PartsDatabase,
        PartsSignalMaster
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
        for gui, db, sig in self._sub_databases:
            db.rollback_to_savepoint()
            gui.refresh()

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

        try:
            parts_sig_master = PartsSignalMaster()
            parts_db = PartsDatabase(os.path.join(dir_path, self._config["parts"]["file"]), parts_sig_master)
            parts_gui = PartsGUI(parts_db, parts_sig_master)
            parts_sig_master.save_state_changed.connect(self._sub_db_save_state_changed)
            self._sub_databases.append((parts_gui, parts_db, parts_sig_master))
            self._signal_master.new_inventory_tab.emit(parts_gui, "Parts")
        except KeyError:
            raise MainDBLoadError("Error in config.json: No parts database specified.")

        for db in self._config["databases"]:
            try:
                classes = db_types[db["type"]]
            except KeyError:
                print("Unknown inventory type found in config.json: Skipping.")
                continue

            sig_master = classes[2]()  # Signal master
            sub_db = classes[1](os.path.join(dir_path, db["file"]), sig_master)  # Database
            gui = classes[0](sub_db, sig_master)  # GUI
            sig_master.save_state_changed.connect(self._sub_db_save_state_changed)  # Connect save state changed signal
            self._sub_databases.append((gui, sub_db, sig_master))  # Store
            self._signal_master.new_inventory_tab.emit(gui, db["file"])  # Emit new tab signal to main GUI

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

        print("Sub db save state changed to False")
        self.saved = False
        self._signal_master.main_save_state_changed.emit(False)
