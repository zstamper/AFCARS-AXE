# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PySide6 port of the widgets/gallery example from Qt v5.15"""

import sys

from PySide6.QtCore import QFile
from PySide6.QtGui import QAction
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QToolButton, QPushButton

import model

from dialogs.childform import ChildForm
from model import TribeTable, OOHRecord, Child, Context, StateTable, TribeStateTable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.form_widget = None
        self.setup_ui()

    def setup_ui(self):
        loader = QUiLoader()
        main_window_file = QFile('ui/mainwindow.ui')
        main_window_file.open(QFile.ReadOnly)
        self.form_widget = loader.load(main_window_file)
        main_window_file.close()

        self.setCentralWidget(self.form_widget)
        self.resize(self.form_widget.baseSize())

        self.form_widget.findChild(QAction, 'actionOpen').triggered.connect(self.open_dialog)
        self.form_widget.findChild(QAction, 'actionQuit').triggered.connect(self.close)
        self.form_widget.findChild(QToolButton, 'importButton').clicked.connect(self.open_dialog)
        self.form_widget.findChild(QPushButton, 'add_child').clicked.connect(self.add_child)

    def add_child(self):
        child_dialog = ChildForm(self)
        query = (StateTable
                 .select()
                 .join(TribeStateTable)
                 .join(TribeTable)
                 .order_by(StateTable.name))
        tribes_by_state = [(row.code, row.tribes) for row in query]
        child_dialog.set_epa_ids(tribes_by_state)
        child_dialog.populate(OOHRecord(child=Child(),
                                        context=Context(),
                                        tribes=[],
                                        second_parents=[],
                                        removals1993=[],
                                        removals2020=[]))
        child_dialog.exec()

    def open_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setWindowTitle('Open Database')
        file_dialog.setDefaultSuffix('.db')
        file_dialog.setNameFilter('AFCARS Databases (*.db)')
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            print(f"Selected files: {selected_files}")


def main():
    model.open_database('default.db')
    model.create_tables()
    app = QApplication()
    with open('ui/style.qss') as f:
        style_sheet = f.read()
    app.setStyleSheet(style_sheet)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
