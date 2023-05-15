import threading

class Singleton(type(QObject), type):
    #_instance = None

    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls._instance = None
    
    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kw)
        return cls._instance