from abc import ABC, abstractmethod
from functools import wraps
from typing import Type

from .signal_master_base import SignalMasterBase


class DatabaseBase(ABC):
    def __int__(self, sig_master: SignalMasterBase) -> None:
        self._saved_val = True
        self._signal_master = sig_master

    @staticmethod
    def changes_db(func):
        """!
        @brief Decorator for functions that change (un-save) the database.
        """
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self._saved = False  # Calls the property setter
            return func(*args, **kwargs)
        return wrapper

    @property
    def _saved(self) -> bool:
        return self._saved_val

    @_saved.setter
    def _saved(self, value: bool) -> None:
        self._signal_master.save_state_changed.emit(value)
        self._saved_val = value

    @abstractmethod
    def load_from_file(self, db_file) -> None:
        """!
        @brief Method to load a database from a file.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """!
        @brief Gracefully close the connection to the database file.
        """
        pass

    @abstractmethod
    def make_savepoint(self) -> None:
        """!
        @brief Create a savepoint to roll back to.
        """
        pass

    @abstractmethod
    def save(self) -> None:
        """!
        @brief Save the current database.
        """
        pass

    @abstractmethod
    def rollback_to_savepoint(self) -> None:
        """!
        @brief Roll back the database to last savepoint.
        """
        pass
