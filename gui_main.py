import re
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import *

import sort
import repo


class Array:
    def __init__(self, id=None, source_array=None, sort_array=None):
        self.id = id
        self.source_array = source_array
        self.sort_array = None if sort_array == "NULL" else sort_array

    def set_source_array(self, source_array):
        self.source_array = source_array

    def set_sort_array(self, sort_array):
        self.sort_array = sort_array


# Значения таблицы QTableWidget
class TableItems:
    def __init__(self, items=None):
        self.items = items

    def setItems(self, items):
        self.items = items


def new_item(value):
    return QTableWidgetItem(value)


# Основной интерфейс приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('heapSort.ui', self)

        self.array_line.setPlaceholderText("Введите массив")

        # Установка триггеров для кнопок
        self.save_button.clicked.connect(self.save_array)
        self.sort_button.clicked.connect(self.sort_array)
        self.show_button.clicked.connect(self.show_all_arrays)
        self.select_button.clicked.connect(self.select_array)
        self.del_button.clicked.connect(self.delete_array)

        # Текущий массив, с которым сейчас ведется работа
        self.current_array = Array()
        self.tableItems = TableItems()

    # Сохранение введеного массива или
    # обновление редактированного массива из БД
    def save_array(self):
        self.hidden_table(True)
        try:
            array_str = self.array_line.text()

            valid_str = self.valid_str(array_str)

            sort_empty = "NULL"
            if self.current_array.id is not None:
                if self.current_array.source_array != valid_str:
                    self.current_array.set_source_array(valid_str)
                    self.current_array.set_sort_array(sort_empty)
                repo.update_array(self.current_array)
            else:
                if (self.current_array.source_array == valid_str and
                        self.current_array.sort_array is not None):
                    sort_empty = self.current_array.sort_array
                repo.insert_array(valid_str, sort_empty)

            self.array_line.setText("")
            self.info_label.setText("Successfully saved")
            self.current_array = Array()
        except Exception as e:
            self.info_label.setText("Save error: " + str(e))

    # Сортировка массива
    def sort_array(self):
        self.hidden_table(True)
        try:
            valid_str = self.valid_str(
                self.array_line.text()
            )
            array = self.str_to_array(valid_str)
            sort.heap_sort(array)
            sorted_str = str(array).strip("[]")

            self.current_array.set_source_array(valid_str)
            self.current_array.set_sort_array(sorted_str)

            self.info_label.setText(sorted_str)
        except Exception as e:
            self.info_label.setText("Sort error: " + str(e))

    # Строку в список значений
    def str_to_array(self, array_str):
        array_str = self.valid_str(array_str)
        return list(map(int, array_str.split(",")))

    # Проверка введенной строки
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

    # Отображение всех массивов из БД
    def show_all_arrays(self):
        # Настройки QTableWidget
        self.table_widget.setRowCount(0)
        self.table_widget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.hidden_table(False)

        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        arrays = self.get_db_arrays()
        self.tableItems.setItems(arrays)
        for i in range(len(arrays)):
            array = arrays[i]
            self.table_widget.insertRow(i)
            self.table_widget.setItem(i, 0, new_item(str(array.id)))
            self.table_widget.setItem(i, 1, new_item(array.source_array))
            self.table_widget.setItem(i, 2, new_item(array.sort_array))

    def get_db_arrays(self):
        raw_arrays = repo.get_arrays()
        return list(map(self.tuple_to_record, raw_arrays))

    # Выбор массива из таблицы
    def select_array(self):
        index = self.table_widget.currentIndex().row()

        if index < 0:
            return

        self.current_array = self.tableItems.items[index]

        self.hidden_table(True)
        self.array_line.setText(self.current_array.source_array)
        self.info_label.setText(self.current_array.sort_array)

    def delete_array(self):
        index = self.table_widget.currentIndex().row()

        if index < 0:
            return

        repo.delete_array(
            self.tableItems.items[index].id
        )
        self.show_all_arrays()

    def tuple_to_record(self, tup):
        return Array(*tup)

    def hidden_table(self, flag):
        self.table_widget.setHidden(flag)
        self.select_button.setHidden(flag)
        self.del_button.setHidden(flag)

        self.info_label.setHidden(not flag)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
