from functools import wraps
from threading import Lock

from PyQt5.Qt import QObject


def changes_db(func):
    """!
    A decorator to describe a function that changes the database.
    Calls the self.unsaved() method to send the saveStateChanged to the editor that it is now not saved anymore.
    """
    @wraps(func)
    def wrapper(self, *args, **kw):
        self._unsaved()
        return func(self, *args, **kw)

    return wrapper


class DBConnectError(Exception):
    """Raised when not able to connect to database"""
    def __init__(self, error_msg: str):
        self._msg = error_msg

    def __repr__(self):
        return f"{self._msg}"


class MainDBLoadError(Exception):
    """Raised when the MainDatabase encounters an error while loading."""


class Singleton(type(QObject), type):
    """!
    @brief A Singleton Metaclass

    Add metaclass=Singleton to class definition to turn into a singleton class.
    Working principle:
    When a new instance of a Singleton class is created the "__call__()" function will be called.
    This function will check for an existing instance of that class in the _instances dictionary.
    If no instance is found, it creates a new one, stores it and returns it. It also uses a thread lock
    to make it multi-threading safe.
    """

    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance

        return cls._instances[cls]
