import os
from datetime import datetime
from typing import Optional

from PySide6.QtCore import QFile, Qt, QDate
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QDialog, QWidget, QErrorMessage, QCheckBox, QRadioButton, QLineEdit, QDateEdit, QComboBox, \
    QButtonGroup
from PySide6.QtWidgets import QMessageBox


class BaseDialog(QDialog):

    def __init__(self,
                 parent: Optional[QWidget] = None,
                 flags: Qt.WindowType = None,
                 relaxed_rules: bool = False):
        if flags is None:
            flags = Qt.WindowType()
        super().__init__(parent, flags)
        self.is_dirty: bool = False
        self.errors: list[str] = []
        self.relaxed_rules = relaxed_rules

    def load_ui(self, file_name: str) -> QWidget:
        ui_file_path = os.path.join(os.path.dirname(__file__), '..', 'ui', file_name)
        loader = QUiLoader()
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file)
        ui_file.close()
        return ui

    def accept(self):
        if not self.relaxed_rules:
            if not self.validate():
                error_message_dialog(self, self.errors)
                return
        self._to_obj()
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

    # TODO: figure out a method that wires up all of the change detection logic for the 'is_dirty' functionality

    def validate(self) -> bool:
        raise NotImplementedError("method validate is not implemented")

    def _to_obj(self):
        raise NotImplementedError("method _to_obj is not implemented")

    def _to_int(self, value: any) -> int | None:
        try:
            return int(value)
        except ValueError:
            return None

    @staticmethod
    def _set_text_field(ui, obj) -> None:
        ui.setText(obj if obj is not None else '')

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
    def _set_combobox_selection(ui: QWidget, obj: int, mapping: int | dict | None = None) -> None:
        if obj is None:
            ui.setCurrentIndex(-1)
        elif mapping is None:
            ui.setCurrentIndex(obj)
        elif type(mapping) == int:
            ui.setCurrentIndex(obj + mapping)
        elif obj in mapping:
            ui.setCurrentIndex(mapping[obj])
        else:
            ui.setCurrentIndex(-1)

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
