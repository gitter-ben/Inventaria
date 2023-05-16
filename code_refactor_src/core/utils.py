from threading import Thread, Lock

from PyQt5.Qt import QObject

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
