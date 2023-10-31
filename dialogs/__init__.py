import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable

from PySide6.QtCore import QFile, Qt, QDate
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QDialog, QWidget, QErrorMessage, QCheckBox, QRadioButton, QLineEdit, QComboBox, \
    QButtonGroup, QTableWidget, QListWidget
from PySide6.QtWidgets import QMessageBox

from .main_window import MainWindow


# class BasePath:
#     _base_path: str | None = None
#
#     @staticmethod
#     def path(new_path: str = None) -> str:
#         if new_path is not None:
#             print(f"{new_path=}")
#             BasePath._base_path = Path(new_path).resolve().parent
#         return str(BasePath._base_path)


class BaseDialog(QDialog):

    def __init__(self,
                 parent: Optional[QWidget] = None,
                 flags: Qt.WindowType | None = None,
                 relaxed_rules: bool = False):
        if flags is None:
            flags = Qt.WindowType()
        super().__init__(parent, flags)
        self.id: int | None = None
        self.is_dirty: bool = False
        self.errors: list[str] = []
        self.relaxed_rules = relaxed_rules
        self._on_accept = None

    def _on_accept(self, v: Callable):
        self._on_accept = v

    on_accept = property(None, _on_accept, None)

    def load_ui(self, file_name: str) -> QWidget:
        if getattr(sys, 'frozen', False):
            # we are running in a bundle
            bundle_dir = sys._MEIPASS
        else:
            # we are running in a normal Python environment
            bundle_dir = Path(__file__).resolve().parent.parent
        ui_file_path = Path(bundle_dir) / 'ui' / file_name
        # print(f"{ui_file_path=}")
        loader = QUiLoader()
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file)
        ui_file.close()
        return ui

    def accept(self):
        if self._on_accept is None or (self._on_accept and self._on_accept()):
            super().accept()

    def reject(self):
        if self.is_dirty:
            ret = reject_confirmation_dialog(self)
            if ret == QMessageBox.Save:
                self.accept()
                return
            elif ret == QMessageBox.Cancel:
                return
        super().reject()

    def clear(self) -> None:
        self.id = None
        for name in dir(self.ui):
            widget = getattr(self.ui, name)
            match widget:
                case QLineEdit():
                    widget.clear()
                case QComboBox():
                    widget.setCurrentIndex(-1)
                case QButtonGroup():
                    for button in widget.buttons():
                        button.setChecked(False)
                case QRadioButton():
                    widget.setChecked(False)
                case QCheckBox():
                    widget.setChecked(False)
                case QTableWidget():
                    widget.clearContents()
                case QListWidget():
                    widget.clear()

    @staticmethod
    def _set_text_field(ui, obj) -> None:
        ui.setText(obj if obj is not None else '')

    @staticmethod
    def _get_text_field(ui) -> str:
        v: str = ui.text()
        return v if v != '' else None

    @staticmethod
    def _set_date_field(ui, obj: datetime | None) -> None:
        date: QDate = QDate(obj.year, obj.month, obj.day) if obj is not None else QDate()
        ui.setDate(date)

    @staticmethod
    def _get_int_field(ui) -> int | None:
        try:
            return int(ui.text())
        except ValueError:
            return None

    @staticmethod
    def _set_int_field(ui, obj) -> None:
        ui.setText(str(obj) if obj is not None else '')

    @staticmethod
    def _get_combobox_text(ui, obj, mapping=None):
        if obj is None:
            return ""
        elif type(mapping) == int and obj + mapping >= 0:
            return ui.itemText(obj + mapping)
        elif type(mapping) == dict and obj in mapping:
            return ui.itemText(mapping[obj])
        return ui.itemText(obj)

    @staticmethod
    def _init_radio(ui: QWidget, name: str, ids: dict) -> None:
        elem: QWidget = ui.__getattribute__(name)
        for k, v in ids.items():
            elem.setId(ui.__getattribute__(f"{name}_{k}"), v)

    @staticmethod
    def _init_radio_mf(ui: QWidget, name: str) -> None:
        BaseDialog._init_radio(ui, name, {'m': 1, 'f': 2})

    @staticmethod
    def _init_radio_yn(ui: QWidget, name: str) -> None:
        BaseDialog._init_radio(ui, name, {'n': 0, 'y': 1})

    @staticmethod
    def _init_radio_ynna(ui: QWidget, name: str) -> None:
        BaseDialog._init_radio(ui, name, {'n': 0, 'y': 1, 'na': 9})

    @staticmethod
    def _init_radio_ynu(ui: QWidget, name: str) -> None:
        BaseDialog._init_radio(ui, name, {'n': 0, 'y': 1, 'u': 9})

    @staticmethod
    def _init_radio_ynud(ui: QWidget, name: str) -> None:
        BaseDialog._init_radio(ui, name, {'n': 0, 'y': 1, 'd': 8, 'u': 9})

    @staticmethod
    def _init_radio_dna(ui: QWidget, name: str) -> None:
        BaseDialog._init_radio(ui, name, {'na': 0, 'a': 1})

    @staticmethod
    def _set_radio_button(ui, obj) -> None:
        if obj is not None:
            btn = ui.button(obj)
            if btn:
                btn.setChecked(True)
                return
        for btn in ui.buttons():
            btn.setChecked(False)

    @staticmethod
    def _get_radio_button(ui: QButtonGroup):
        return ui.checkedId() if ui.checkedId() >= 0 else None

    @staticmethod
    def _set_combobox_selection(widget: QWidget, obj: int, mapping: int | dict | None = None) -> None:
        if obj is None:
            widget.setCurrentIndex(-1)
        elif mapping is None:
            widget.setCurrentIndex(obj)
        elif type(mapping) == int:
            widget.setCurrentIndex(obj + mapping)
        elif obj in mapping:
            widget.setCurrentIndex(mapping[obj])
        else:
            widget.setCurrentIndex(-1)

    @staticmethod
    def _get_combobox_selection(ui: QComboBox, mapping: int | dict | None = None) -> int | None:
        current_index = ui.currentIndex()
        if current_index is None or current_index == -1:
            return None
        if mapping is None:
            return current_index if current_index >= 0 else None
        if type(mapping) == int:
            return current_index + mapping
        return mapping[current_index]


def reject_confirmation_dialog(parent: QWidget) -> int:
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle("Confirm")
    msg_box.setText("The record has been modified.")
    msg_box.setInformativeText("Do you want to save your changes?")
    msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
    msg_box.setDefaultButton(QMessageBox.Save)
    return msg_box.exec()


def delete_confirmation_dialog(parent: QWidget) -> int:
    result: QMessageBox.StandardButton = QMessageBox.warning(parent, "Confirm",
                                                             "Are you sure you want<br/>to delete this record?",
                                                             QMessageBox.Yes,
                                                             QMessageBox.No)
    return result == QMessageBox.Yes


def error_message_dialog(parent: QWidget, errors: list[str]):
    err_box = QErrorMessage(parent)
    err_box.showMessage("\n\n- ".join(errors))
    err_box.setWindowTitle("Error")
    err_box.exec()
