# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PySide6 port of the widgets/gallery example from Qt v5.15"""

import sys

from PySide6.QtCore import QFile
from PySide6.QtGui import QAction
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QToolButton, QPushButton, QTableWidgetItem, \
    QTableWidget

import model
from controllers import GenericController, OOHController
from controllers.a_controller import AController
from dialogs.a_dialog import ADialog

from dialogs.ooh_dialog import OOHDialog
from model import TribeTable, OOHRecord, Child, Context, StateTable, TribeStateTable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = None
        self.setup_ui()
        self._children = []
        self.setWindowTitle('AFCARS Database Tool')
        self.context_id = 1  # FIXME: need to fetch context ID from the Context table

    def setup_ui(self):
        loader = QUiLoader()
        main_window_file = QFile('ui/mainwindow.ui')
        main_window_file.open(QFile.ReadOnly)
        self.ui = loader.load(main_window_file)
        main_window_file.close()

        self.setCentralWidget(self.ui)
        self.resize(self.ui.baseSize())

        self.ui.findChild(QAction, 'actionOpen').triggered.connect(self.open_dialog)
        self.ui.findChild(QAction, 'actionQuit').triggered.connect(self.close)
        self.ui.findChild(QToolButton, 'importButton').clicked.connect(self.open_dialog)
        self.ui.findChild(QPushButton, 'add_child').clicked.connect(self.add_ooh)
        self.ui.findChild(QTableWidget, 'child_table').doubleClicked.connect(self.edit_ooh)

    def add_a(self):
        a_dialog = ADialog(self)
        controller = AController(a_dialog, self.context_id)
        data: Child = controller.add()
        if data is not None:
            self._children.append(data)
            self.__add_child_row(data)

    def edit_a(self):
        current_row = self.ui.child_table.currentRow()
        if current_row >= 0:
            data = self._children[current_row]
            dialog = ADialog(self)
            controller = AController(dialog, self.context_id)
            controller.edit(data)
            self.__update_child_row(current_row, data)

    def edit_a_button_clicked(self):
        row = self.sender().property('row')
        self.ui.child_table.setCurrentCell(row,6)
        self.edit_a()

    def delete_a(self):
        current_row = self.ui.child_table.currentRow()
        if 0 <= current_row < len(self._children):
            del self._children[current_row]
            self.ui.child_table.removeRow(current_row)

    def add_ooh(self):
        ooh_dialog = OOHDialog(self)
        controller = OOHController(ooh_dialog, self.context_id)
        data: Child = controller.add()
        if data is not None:
            self._children.append(data)
            self.__add_child_row(data)

    def edit_ooh(self):
        current_row = self.ui.child_table.currentRow()
        if current_row >= 0:
            data = self._children[current_row]
            dialog = OOHDialog(self)
            dialog.setWindowTitle(f"{data.last_name}, {data.first_name}")
            controller = OOHController(dialog, self.context_id)
            controller.edit(data)
            self.__update_child_row(current_row, data)

    def edit_ooh_button_clicked(self):
        row = self.sender().property('row')
        self.ui.child_table.setCurrentCell(row,5)
        self.edit_ooh()

    def delete_ooh(self):
        current_row = self.ui.child_table.currentRow()
        if 0 <= current_row < len(self._children):
            del self._children[current_row]
            self.ui.child_table.removeRow(current_row)

    def __add_child_row(self, data: Child):
        row: int = self.ui.child_table.rowCount()
        self.ui.child_table.insertRow(row)
        self.__update_child_row(row, data)

    def __update_child_row(self, row: int, data: Child):
        self.ui.child_table.setItem(row, 0, QTableWidgetItem(data.e4))
        self.ui.child_table.setItem(row, 1, QTableWidgetItem(data.last_name))
        self.ui.child_table.setItem(row, 2, QTableWidgetItem(data.first_name))
        self.ui.child_table.setItem(row, 3, QTableWidgetItem('M' if data.e6 == 1 else 'F' if data.e6 == 2 else ''))
        self.ui.child_table.setItem(row, 4, QTableWidgetItem(str(data.e5)))
        button = QPushButton('Add' if data.ooh is None else 'Edit')
        button.clicked.connect(self.edit_ooh_button_clicked)
        button.setProperty('row', row)
        self.ui.child_table.setCellWidget(row, 5, button)
        button = QPushButton('Add' if data.a is None else 'Edit')
        button.clicked.connect(self.edit_a_button_clicked)
        self.ui.child_table.setCellWidget(row, 6, button)
        button.setProperty('row', row)

    def refresh_children(self):
        for child in self._children:
            self.__add_child_row(child)

    def open_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setWindowTitle('Open Database')
        file_dialog.setDefaultSuffix('.db')
        file_dialog.setNameFilter('AFCARS Databases (*.db)')
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            print(f"Selected files: {selected_files}")


def inject_demo_data(dialog):
    dialog._children.append(
        Child(id=None, context_id=1, last_name="Rubble", first_name="Barney", e4="000000000000", e5=1, e6=20050606,
              e13=None, e14=None, e15=None, e16=None, e17=None, e18=None, e19=None, e20=None,
              e21=None, ooh=None, a=None))


def main():
    model.open_database('default.db')
    model.create_tables()
    app = QApplication()
    app.setApplicationName('ADT')
    app.setApplicationDisplayName('ADT')
    app.setDesktopFileName('ADT')
    with open('ui/style.qss') as f:
        style_sheet = f.read()
    app.setStyleSheet(style_sheet)
    main_window = MainWindow()
    inject_demo_data(main_window)
    main_window.refresh_children()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
