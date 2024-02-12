import re
import sys

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import *

import main
import repo


class Array:

    def __init__(self, source_array, sort_array=None):
        self.source_array = source_array
        self.sort_array = sort_array

    def get_source_array(self):
        return self.source_array

    def get_sort_array(self):
        return self.sort_array


class MainWindow(QMainWindow):
    pyqt_clicked = pyqtSignal()

    # last_array = Array

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('heapSort.ui', self)
        # self.table_widget.setHidden(True)
        # self.info_label.setText("NewText")
        # self.pyqt_clicked.connect(button)
        self.save_button.clicked.connect(self.save_array)
        self.sort_button.clicked.connect(self.sort_array)

        self.last_array = None

    def on_but(self):
        # info = self.info_label = QLabel

        self.info_label.setText("On button")

    def save_array(self):
        try:
            array_str = self.array_line.text()

            valid_str = self.valid_str(array_str)
            sorted_str = "NULL"
            if (self.last_array is not None and
                    self.last_array.get_source_array() == valid_str and
                    self.last_array.get_sort_array() is not None):
                sorted_str = self.last_array.get_sort_array()

            repo.insert_array(valid_str, sorted_str)

            self.array_line.setText("")
            self.info_label.setText("Successfully saved")
        except Exception as e:
            self.info_label.setText("Save error: " + str(e))

    def sort_array(self):
        try:
            valid_str = self.valid_str(
                self.array_line.text()
            )
            array = self.str_to_array(valid_str)
            main.heap_sort(array)
            sorted_str = str(array).strip("[]")

            self.last_array = Array(valid_str, sorted_str)
            self.info_label.setText(sorted_str)
        except Exception as e:
            self.info_label.setText("Sort error: " + str(e))

    def str_to_array(self, array_str):
        array_str = self.valid_str(array_str)
        return list(map(int, array_str.split(",")))

    def valid_str(self, raw_str):
        if len(raw_str) == 0:
            raise Exception("Empty line")
        if not re.fullmatch("[0-9,.\\s]+", raw_str):
            self.array_line.setText("")
            raise Exception("Invalid array")
        return re.sub(
            ",{2,}", ",",
            raw_str.strip(", ")
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
