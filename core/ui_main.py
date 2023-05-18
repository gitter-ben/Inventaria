from typing import Tuple

from PyQt5.Qt import (
    QAction,
)
from PyQt5.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QProgressBar
)

from inventory_types import *
from core.constants import *
from database import MainDatabase
from resources import resources


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nothing(resources.qt_version)

        self._global_signal_master = GlobalSignalMaster()

        self._db_loaded = False
        self._db = MainDatabase(self._global_signal_master)

        self._inventories: List[Tuple[GroupsAndBoxesSignalMaster, GroupsAndBoxesDatabase, GroupsAndBoxesGUI], ...] = []

        self.__setup_gui()

    @staticmethod
    def nothing(x):
        """!
        This method's sole purpose is the elimination of an unused import warning
        because it can't see that resources/resources.py is being used. Without that
        import the images and icons wouldn't work.
        """
        return x

    def __setup_gui(self) -> None:
        """!
        @brief Initialize the main GUI of Inventaria.

        Steps:
        1. Set application settings and top layout
        2. Make menubar and statusbar
        3. Make top bar with save, load, rollback, ...
        4. Make inventory tabs
        5. Make bottom bar
        """
        # ======= Set application settings =======
        self.setWindowTitle(APPLICATION_TITLE)
        self.resize(INITIAL_WINDOW_WIDTH, INITIAL_WINDOW_HEIGHT)
        self.setStyleSheet("""
            QSplitter::handle { background-color: #AAAAAA; }
            QTabWidget, QTabBar { background-color: #C8C8C8; }
        """)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(200, 200, 200))
        self.setPalette(palette)

        main_splitter = QSplitter(Qt.Vertical)
        self.setCentralWidget(main_splitter)
        # ========================================

        # ======= Make menu- and statusbar =======
        open_action = QAction("&Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Open a file")
        open_action.triggered.connect(self._load_db_slot)

        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip("Save the current database")
        save_action.triggered.connect(self._save_slot)

        unload_action = QAction("&Unload", self)
        unload_action.setStatusTip("Unload the current database")
        unload_action.triggered.connect(self._unload_db_slot)

        roll_back_action = QAction("&Rollback", self)
        roll_back_action.setStatusTip("Undo all changes since last save")
        roll_back_action.triggered.connect(self._roll_back_slot)

        quit_action = QAction("&Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.setStatusTip("Quit the application")
        quit_action.triggered.connect(self.close)

        preferences_action = QAction("&Preferences")
        preferences_action.setShortcut("Ctrl+P")
        preferences_action.setStatusTip("Show the preferences")
        preferences_action.triggered.connect(self._show_preferences_slot)

        about_action = QAction("&About", self)
        about_action.setStatusTip("Show the about section")
        about_action.triggered.connect(self._show_about_slot)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(save_action)
        file_menu.addAction(open_action)
        file_menu.addAction(unload_action)
        file_menu.addAction(roll_back_action)
        file_menu.insertSeparator(quit_action)
        file_menu.addAction(quit_action)
        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction(preferences_action)
        # tools_menu = menu_bar.addMenu("&Tools")
        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction(about_action)
        # ========================================

        # ============= Make top bar =============
        top_bar = QWidget()
        top_bar_layout = QGridLayout()
        ic = QIcon(":/icons/open_file_icon.png")
        load_button = QPushButton("Load")
        load_button.setFixedWidth(82)
        load_button.setIcon(ic)
        load_button.pressed.connect(self._load_db_slot)
        top_bar_layout.addWidget(load_button, 0, 0, 1, 1)
        ic = QIcon(":/icons/save_icon.png")
        save_button = QPushButton("Save")
        save_button.setFixedWidth(82)
        save_button.setIcon(ic)
        save_button.pressed.connect(self._save_slot)
        top_bar_layout.addWidget(save_button, 0, 1, 1, 1)
        ic = QIcon(":/icons/rollback_icon.png")
        roll_back_button = QPushButton("Rollback")
        roll_back_button.setFixedWidth(82)
        roll_back_button.setIcon(ic)
        roll_back_button.pressed.connect(self._roll_back_slot)
        top_bar_layout.addWidget(roll_back_button, 0, 2, 1, 1)

        top_bar_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_bar.setLayout(top_bar_layout)
        top_bar.setFixedHeight(TOP_BAR_HEIGHT)
        main_splitter.addWidget(top_bar)
        # ========================================

        # ======= Make inventory type tabs ========
        inventory_gui_tabs = QTabWidget()
        self._test_add_inventory()
        inventory_gui_tabs.addTab(self._inventories[0][2], "Groups and Boxes 1")
        main_splitter.addWidget(inventory_gui_tabs)
        # =========================================

        # =========== Make bottom bar =============
        bottom_bar = QWidget()
        bottom_bar_layout = QHBoxLayout()
        bottom_bar_layout.setSpacing(25)
        self._saved_indicator = QLabel("No database")
        bottom_bar_layout.addWidget(self._saved_indicator)
        self._current_job_label = QLabel("Current Job: None")
        bottom_bar_layout.addWidget(self._current_job_label)
        self._job_progress_bar = QProgressBar()
        bottom_bar_layout.addWidget(self._job_progress_bar)
        bottom_bar.setLayout(bottom_bar_layout)
        bottom_bar.setFixedWidth(40)
        main_splitter.addWidget(bottom_bar)
        # =========================================

    def _test_add_inventory(self) -> None:
        sig_master = GroupsAndBoxesSignalMaster()
        db = GroupsAndBoxesDatabase("../groups_and_boxes.sqlite", sig_master)
        gui = GroupsAndBoxesGUI(db, sig_master, self._global_signal_master)

        self._inventories.append((sig_master, db, gui))

    def closeEvent(self, event):
        if self._db_loaded:
            if not self._db.saved:
                reply = QMessageBox.question(
                    self,
                    "Close without saving",
                    "Are you sure you want to close without saving?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    self._db.close()
                    event.accept()
                else:
                    event.ignore()
            else:
                self._db.close()
                event.accept()

    @pyqtSlot()
    def _load_db_slot(self):
        print("DB loaded.")

    @pyqtSlot()
    def _save_slot(self):
        print("Saved.")

    @pyqtSlot()
    def _unload_db_slot(self):
        print("DB unloaded.")

    @pyqtSlot()
    def _roll_back_slot(self):
        print("DB rolled back.")

    @pyqtSlot()
    def _show_preferences_slot(self):
        print("Preferences showed.")

    @pyqtSlot()
    def _show_about_slot(self):
        print("About showed.")
