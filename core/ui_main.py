"""!
@file ui_main.py
@brief The main file for the application GUI and logic.
"""

from textwrap import dedent

from PyQt5.Qt import (
    QAction,
    QPalette,
    QColor,
    QIcon,
    pyqtSlot
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QMessageBox,
    QLabel,
    QMainWindow,
    QTabWidget,
    QProgressBar,
    QVBoxLayout,
    QFrame,
    QFileDialog,
    QPushButton,
)

from core.constants import *
from core.signal_master import MainSignalMaster
from core.database import MainDatabase
from core.utils import MainDBLoadError
from resources import resources


class MainWindow(QMainWindow):
    """!
    @brief Class to define the GUI and logic of the Inventaria main window.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nothing(resources.qt_version)

        self._global_signal_master = MainSignalMaster()

        self._db_loaded = False
        self._db = None

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
        4. Make line
        5. Make inventory tabs
        6. Make second line
        7. Make bottom bar
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

        main_layout = QVBoxLayout()
        (main_widget := QWidget()).setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(main_widget)
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
        save_button.setEnabled(False)
        top_bar_layout.addWidget(save_button, 0, 1, 1, 1)
        ic = QIcon(":/icons/rollback_icon.png")
        roll_back_button = QPushButton("Rollback")
        roll_back_button.setFixedWidth(82)
        roll_back_button.setIcon(ic)
        roll_back_button.pressed.connect(self._roll_back_slot)
        roll_back_button.setEnabled(False)
        top_bar_layout.addWidget(roll_back_button, 0, 2, 1, 1)

        top_bar_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_bar_layout.setContentsMargins(8, 0, 8, 0)
        top_bar.setLayout(top_bar_layout)
        top_bar.setFixedHeight(TOP_BAR_HEIGHT)
        main_layout.addWidget(top_bar)
        # ========================================

        # ============ Make line =================
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setLineWidth(5)
        line.setStyleSheet("color: #AAAAAA")
        main_layout.addWidget(line)
        # ========================================

        # ======= Make inventory type tabs =======
        self._inventory_gui_tabs = QTabWidget()
        self._inventory_gui_tabs.setStyleSheet("QTabWidget::pane { border: 0 };")
        main_layout.addWidget(self._inventory_gui_tabs)
        # ========================================

        # ============ Make line 2 ===============
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setLineWidth(5)
        line.setStyleSheet("color: #AAAAAA")
        main_layout.addWidget(line)
        # ========================================

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
        bottom_bar.setFixedHeight(40)
        main_layout.addWidget(bottom_bar)
        # =========================================

    def closeEvent(self, event) -> None:
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
    def _load_db_slot(self) -> None:
        directory_name = str(QFileDialog.getExistingDirectory(self, "Select directory"))
        try:
            self._db = MainDatabase(directory_name, self._global_signal_master)
        except MainDBLoadError as e:
            self._show_message("Error", f"There was an error loading the database:\n{e}")
            return
        print("DB loaded.")

    @pyqtSlot()
    def _save_slot(self) -> None:
        if not self._db_loaded:
            self._show_message("Error", "No database to save.")
            return

        print("Saved.")

    @pyqtSlot()
    def _unload_db_slot(self) -> None:
        if not self._db_loaded:
            self._show_message("Error", "No database to unload.")
            return

        print("DB unloaded.")

    @pyqtSlot()
    def _roll_back_slot(self) -> None:
        if not self._db_loaded:
            self._show_message("Error", "No database to roll back.")
            return

        print("DB rolled back.")

    @pyqtSlot()
    def _show_preferences_slot(self) -> None:
        print("Preferences showed.")

    @pyqtSlot()
    def _show_about_slot(self) -> None:
        self.about_window = self.AboutWindow(self)
        self.about_window.show()
        print("About showed.")

    def _show_message(self, title, msg) -> None:
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(msg)
        dlg.show()

    class AboutWindow(QWidget):
        """!
        @brief A window to show the about information.
        """
        def __init__(self, parent):
            super().__init__()

            self._parent = parent
            self.setWindowTitle("About")
            self.resize(100, 100)
            layout = QVBoxLayout()
            layout.setAlignment(Qt.AlignCenter)
            main_text = QLabel(dedent("""\
            License: Gnu General Public License
            
            Author: Benjamin Lucas Krüger\
            """))
            layout.addWidget(main_text)
            self.setLayout(layout)

        def showEvent(self, e) -> None:
            if not e.spontaneous():
                geo = self.geometry()
                geo.moveCenter(self._parent.geometry().center())
                QTimer.singleShot(0, lambda: self.setGeometry(geo))
