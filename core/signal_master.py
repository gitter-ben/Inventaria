"""!
@file signal_master.py
@brief Includes the MainSignalMaster class for the application.
"""
from PyQt5.Qt import QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget


class MainSignalMaster(QObject):
    """!
    @brief Signal master for the main window and database.
    """
    main_save_state_changed = pyqtSignal(bool)
    # sub_database_changed = pyqtSignal()
    new_inventory_tab = pyqtSignal(QWidget, str)
