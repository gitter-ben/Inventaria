"""!
@file gui.py
@brief Contains the GUI-classes for the parts inventory type.
"""
from typing import List

from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QWidget,
    QHBoxLayout, QGridLayout, QLabel, QPushButton, QSplitter, QLineEdit
)
from PyQt5.QtCore import Qt

from .database import PartsDatabase
from .signal_master import PartsSignalMaster
from .common import Part


class PartsGUI(QWidget):
    """!
    @brief The GUI for the parts inventory type.
    """
    def __init__(self, database: PartsDatabase, sig_master: PartsSignalMaster):
        super().__init__()

        self._db = database
        self._signal_master = sig_master

        self._make_gui()

    def refresh(self):
        self._parts_list.clear()
        self._parts_list.populate(self._db.get_parts())

    def _make_gui(self) -> None:
        """!
        @brief Create the GUI for the parts inventory type.
        """

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        splitter = QSplitter(Qt.Vertical)
        splitter.setChildrenCollapsible(False)

        top_bar = QWidget()
        top_bar_layout = QGridLayout()
        top_bar_layout.setContentsMargins(5, 5, 5, 5)
        top_bar_layout.addWidget(new_part_label := QLabel("New part: "), 0, 0, 1, 1)
        top_bar_layout.addWidget(new_part_name_edit := QLineEdit(), 0, 1, 1, 1)
        top_bar_layout.addWidget(new_part_button := QPushButton("Make part"), 0, 2, 1, 1)

        def new_part():
            if len(text := new_part_name_edit.text()) == 0:
                return

            self._db.add_part(text)
            self.refresh()

        new_part_button.clicked.connect(new_part)

        @pyqtSlot(int)
        def delete_part_slot(part_id: int) -> None:
            self._db.delete_part(part_id)
            self.refresh()

        self._signal_master.delete_part.connect(delete_part_slot)

        top_bar.setLayout(top_bar_layout)
        top_bar.setFixedHeight(top_bar.minimumSizeHint().height())
        splitter.addWidget(top_bar)

        self._parts_list = self.PartsList(self._signal_master)
        self._parts_list.populate(self._db.get_parts())
        splitter.addWidget(self._parts_list)
        layout.addWidget(splitter)
        self.setLayout(layout)

    class PartsList(QListWidget):
        class PartsListItem(QWidget):
            def __init__(self, part: Part, color, sig_master: PartsSignalMaster, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._signal_master = sig_master

                self.id = part.id
                p = self.palette()
                p.setColor(self.backgroundRole(), Qt.black)
                self.setAutoFillBackground(True)
                self.setPalette(p)

                self.setStyleSheet(f"""
                QLabel {{ background-color: {color} }}
                QWidget {{ background-color: {color} }}
                
                . {{ background-color: {color} }}
                """)

                layout = QGridLayout()
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(name_label := QLabel(part.name), 0, 0, 1, 1, alignment=Qt.AlignLeft)
                layout.addWidget(delete_button := QPushButton("Delete"), 0, 1, 1, 1, alignment=Qt.AlignRight)
                delete_button.clicked.connect(lambda: self._signal_master.delete_part.emit(self.id))

                name_label.setContentsMargins(3, 3, 3, 3)
                self.setLayout(layout)

        def __init__(self, signal_master: PartsSignalMaster, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._signal_master = signal_master
            self.setSortingEnabled(True)
            self._items = []

        def clear_items(self):
            self.clear()
            self._items = []

        def populate(self, parts: List[Part]):
            color = "#FFFFFF"
            for part in parts:
                item = QListWidgetItem(self)
                self.addItem(item)
                widget = self.PartsListItem(part, color, self._signal_master)
                self._items.append(widget)
                item.setSizeHint(widget.minimumSizeHint())
                self.setItemWidget(item, widget)
                color = "#AAAAAA" if color == "#FFFFFF" else "#FFFFFF"
