"""!
@file database.py
@brief Includes the MainDatabase class for the application.
"""
from core.signal_master import MainSignalMaster
from core.utils import MainDBLoadError


class MainDatabase:
    """!
    @brief The main database class for Inventaria.

    Database directory layout:
    - config.json: Includes the config for the database, contains list of sub-databases and filenames.
    - databases: Includes all sub-databases
      - <id>_<inventory_type>.sqlite: Name format for sub-databases
      - ...
    - parts.sqlite: The database for all shared parts.
    """
    def __init__(self, directory_path: str, sig_master: MainSignalMaster, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._signal_master = sig_master
        self.saved = True

        raise MainDBLoadError("Some error I guess, I don't really know")

    def new(self, path):
        pass

    def close(self):
        pass
