from abc import ABCMeta, abstractmethod
from functools import wraps


class DBBaseClass(metaclass=ABCMeta):
    @staticmethod
    def changes_db(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self._unsaved()
            return func(self, *args, **kwargs)
        return wrapper

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

    @abstractmethod
    def _unsaved(self) -> None:
        """!
        @brief Method called by the @changesDB decorator.
        """
        pass
