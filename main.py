# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PySide6 port of the widgets/gallery example from Qt v5.15"""
import datetime
import traceback

import peewee

from controllers.main_window2_controller import MainWindow2Controller
from model.models import Tribe

try:
    import os
    import sys
    from pathlib import Path

    from PySide6.QtCore import QFile, QCoreApplication
    from PySide6.QtGui import QAction, QPixmap, QColor
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QToolButton, QPushButton, QTableWidgetItem, \
        QTableWidget, QSplashScreen

    import model
    from controllers.ooh_controller import OOHController
    from controllers.a_controller import AController
    from model import TribeTable, OOHRecord, Child, Context, ContextTable, StateTable, TribeStateTable, BaseChildTable


    def initialize_database() -> None:
        model.create_tables()


    def epa_tribes() -> list[Tribe]:
        results = {}
        query = TribeTable.select().order_by(TribeTable.tribe).prefetch(TribeStateTable, StateTable)
        return [Tribe(id=tribe.id, tribe=tribe.tribe, epa_code=tribe.epa_code, states=[tribestate.state.code for tribestate in tribe.states])
                for tribe in TribeTable.select().order_by(TribeTable.tribe).prefetch(TribeStateTable, StateTable)]
        # for tribe in query:
        #     states = ", ".join([state.state.code for state in tribe.states])
        #     results[tribe.id] = f"{tribe.tribe} ({states})"
        # return results

    def main():
        """
        @startuml
        start
        :show splash page;
        :open the database;
        :populate the child list
        in the main form;
        :show the form;
        :execute event loop;
        end
        @enduml
        """
        try:
            app = QApplication()
            app.setApplicationName('AXE')
            app.setApplicationDisplayName('AXE')
            app.setDesktopFileName('AXE')

            if getattr(sys, 'frozen', False):
                bundle_dir = sys._MEIPASS
            else:
                bundle_dir = os.path.dirname(os.path.abspath(__file__))

            pixmap = QPixmap(Path(bundle_dir) / "assets" / "pexels-negative-space-97077.jpg")
            splash = QSplashScreen(pixmap)
            splash.show()
            splash.showMessage("Opening database...", color=QColor.fromRgb(255, 255, 255, 255))
            QCoreApplication.processEvents()

            with open(Path(bundle_dir) / 'ui' / 'style.qss', 'r') as f:
                style_sheet = f.read()
            app.setStyleSheet(style_sheet)

            if getattr(sys, 'frozen', False):
                database_path = Path.home() / 'axe.db'
            else:
                database_path = 'axe.db'
            model.open_database(str(database_path))

            try:
                if ContextTable.select().count() == 0:
                    splash.showMessage("Initializing new database...", color=QColor.fromRgb(255, 255, 255, 255))
                    QCoreApplication.processEvents()
                    initialize_database()
            except (peewee.OperationalError, peewee.DoesNotExist) as e:
                splash.showMessage("Initializing new database...", color=QColor.fromRgb(255, 255, 255, 255))
                QCoreApplication.processEvents()
                initialize_database()

            main_window = MainWindow2Controller()
            main_window.show()
            splash.finish(main_window.window)
            sys.exit(app.exec())

        except Exception as e:
            traceback.print_exc()
            with open('stderr.txt', 'w+') as stderr:
                print(datetime.time.strftime("%Y-%m-%d %H:%M:%S"), file=stderr)
                traceback.print_exc(file=stderr)
                print('-'*80, file=stderr)


    if __name__ == '__main__':
        main()

except Exception as e:
    traceback.print_exc()
    with open('stderr.txt', 'w') as stderr:
        print(datetime.time.strftime("%Y-%m-%d %H:%M:%S"), file=stderr)
        traceback.print_exc(file=stderr)
        print('-' * 80, file=stderr)
