"""!
@file utils.py
@brief Includes useful things used in lots of files.
"""


class DBConnectError(Exception):
    """!
    @brief Raised when not able to connect to an sqlite database.
    """
    def __init__(self, error_msg: str):
        self._msg = error_msg

    def __repr__(self):
        return f"{self._msg}"


class MainDBLoadError(Exception):
    """!
    @brief Raised when the MainDatabase encounters an error while loading.
    """

