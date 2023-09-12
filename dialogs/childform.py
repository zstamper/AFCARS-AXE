# -*- coding: utf-8 -*-
from string import Template

# from .childform import Ui_ChildForm
from PySide6.QtCore import (Qt, QRegularExpression)
from PySide6.QtGui import (QRegularExpressionValidator)
from PySide6.QtWidgets import (QAbstractButton, QWidget, QListWidgetItem, QTableWidgetItem, QButtonGroup, QDialog,
                               QMessageBox, QTableWidget)

from model import OOHRecord, SecondParent, RecognizedTribe, Removal1993, Removal2020
from utils import generate_id, coalesce
from . import BaseDialog, reject_confirmation_dialog, error_message_dialog, delete_confirmation_dialog
from .Parent2Dialog import Parent2Dialog
from .reject_confirmation import reject_confiration
from .removal1993 import Removal1993Dialog
from .removal2020 import Removal2020Dialog


class ChildModelMappings:
    MALE_FEMALE: dict = {'M': 1, 'F': 2, 'Male': 1, 'Female': 2}
    NA_A: dict = {'Does not apply': 0, 'Applies': 1}
    TPR: dict = {'Not applicable': 0, 'Voluntary': 1, 'Involuntary': 2}
    YES_NO: dict = {'No': 0, 'Yes': 1}
    YES_NO_ABANDONED: dict = {'No': 0, 'Yes': 1, 'Abandoned': 7}
    YES_NO_NA: dict = {'No': 0, 'Yes': 1, 'Not applicable': 9}
    YES_NO_UNKNOWN: dict = {'No': 0, 'Yes': 0, 'Unknown': 9}


class ChildForm(BaseDialog):
    ERROR_TEMPLATE: Template = Template(
        '<html><head/><body><p><span style="font-weight:700; color: #ff2600;">$message</span></p></body></html>')
    E24_ERROR_MESSAGE: str = "At least one of E24 - E34 is required."
    E43_ERROR_MESSAGE: str = "Required."
    E57_ERROR_MESSAGE: str = "Siblings in placement (E57) may not be more<br/>than total siblings (E56)."

    E155_MESSAGES: dict = {1: "Reunify with parent or legal guardian",
                           2: "Live with other relative",
                           3: "Adoption",
                           4: "Emancipation",
                           5: "Guardianship",
                           6: "Runaway or whereabouts unknown",
                           7: "Death of child",
                           8: "Transfer to another agency",
                           9: "Not applicable"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui: QWidget = self.load_ui('ui_childform.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        # Virtual elements:
        # e41 & e44 default to 'no' (0) because the corresponding line edit fields default to empty
        self.e41: int = 0
        self.e44: int = 0
        self.tribes: iter = None
        self.obj: OOHRecord | None = None
        self.recognized_tribes: list = []
        self.second_parents: list[SecondParent] = []
        self.removals1993: list[Removal1993] = []
        self.removals2020: list[Removal2020] = []

    def populate(self, obj: OOHRecord):
        self.obj = obj
        self._from_obj()
        self.errors = []
        self.is_dirty = False
        self._e24_error_refresh()
        self._e43_error_refresh()

    def validate(self):
        self._validate()
        return len(self.errors) == 0

    # ==================================================================================================================

    def set_epa_ids(self, tribe_iterator: iter):
        self.tribes = tribe_iterator
        for state, tribes in tribe_iterator:
            for tribe in tribes:
                item = QListWidgetItem(f"{state} - {tribe.tribe}")
                self.ui.e9.addItem(QListWidgetItem(item))

    # ==================================================================================================================

    def _wire_ui(self):
        ui = self.ui

        self._init_radio_mf(ui, 'e6')
        self._init_radio_yn(ui, 'funding')
        self._init_radio_yn(ui, 'e7')
        self._init_radio_ynu(ui, 'e8')
        self._init_radio_ynu(ui, 'e10')
        self._init_radio_yn(ui, 'e12')
        self._init_radio_yn(ui, 'e22')
        self._init_radio_ynu(ui, 'e61')
        self._init_radio_ynu(ui, 'e62')
        self._init_radio(ui, 'e63', {'na': 0, 'v': 1, 'i': 2})
        self._init_radio_yn(ui, 'e55')
        self._init_radio_yn(ui, 'e106')
        self._init_radio_yn(ui, 'e109')

        "Set-up business rules implemented at UI level"
        ui.form_action.accepted.connect(self.accept)
        ui.form_action.rejected.connect(self.reject)

        ui.last_name.textChanged.connect(self._last_name_text_changed)
        ui.first_name.textChanged.connect(self._first_name_text_changed)

        ui.funding.buttonClicked.connect(self._funding_button_clicked)

        ui.e4.textChanged.connect(self._e4_text_changed)
        ui.e4.setValidator(QRegularExpressionValidator(QRegularExpression(r'[0-9a-zA-Z]{12}')))
        ui.e4_generate.clicked.connect(self._e4_generate_clicked)

        ui.e6.buttonClicked.connect(self._e6_button_clicked)
        ui.e7.buttonClicked.connect(self._e7_button_clicked)
        ui.e8.buttonClicked.connect(self._e8_button_clicked)
        ui.e9.itemClicked.connect(self._e9_item_clicked)
        ui.e10.buttonClicked.connect(self._e10_button_clicked)
        ui.e11.textChanged.connect(self._e11_text_changed)
        ui.e12.buttonClicked.connect(self._e12_button_clicked)

        ui.e19.toggled.connect(self._e19_toggled)
        ui.e20.toggled.connect(self._e20_toggled)

        ui.e23.currentIndexChanged.connect(self._e23_current_index_changed)
        ui.e24.currentIndexChanged.connect(self._e24_error_refresh)
        ui.e25.currentIndexChanged.connect(self._e24_error_refresh)
        ui.e26.currentIndexChanged.connect(self._e24_error_refresh)
        ui.e27.currentIndexChanged.connect(self._e24_error_refresh)
        ui.e28.currentIndexChanged.connect(self._e24_error_refresh)
        ui.e29.currentIndexChanged.connect(self._e24_error_refresh)
        ui.e30.currentIndexChanged.connect(self._e24_error_refresh)
        ui.e31.currentIndexChanged.connect(self._e24_error_refresh)
        ui.e32.currentIndexChanged.connect(self._e24_error_refresh)
        ui.e33.currentIndexChanged.connect(self._e24_error_refresh)
        ui.e34.currentIndexChanged.connect(self._e24_error_refresh)

        ui.e42.textChanged.connect(self._e42_text_changed)
        ui.e45.textChanged.connect(self._e45_text_changed)

        ui.e56.textChanged.connect(self._set_state_e57)
        ui.e57.textChanged.connect(self._set_state_e57)

        ui.parent2_add_button.clicked.connect(self._parent2_add_button_clicked)
        ui.parent2_edit_button.clicked.connect(self._parent2_edit_button_clicked)
        ui.parent2tpr.cellDoubleClicked.connect(self._parent2tpr_cell_double_clicked)

        ui.removal_1993_add_button.clicked.connect(self._removal_1993_add_button_clicked)
        ui.removal_1993_edit_button.clicked.connect(self._removal_1993_edit_button_clicked)
        ui.removal_1993_delete_button.clicked.connect(self._removal_1993_delete_button_clicked)
        ui.removal_1993_table.cellDoubleClicked.connect(self._removal_1993_cell_double_clicked)
        ui.removal_2020_add_button.clicked.connect(self._removal_2020_add_button_clicked)
        ui.removal_2020_edit_button.clicked.connect(self._removal_2020_edit_button_clicked)
        ui.removal_2020_delete_button.clicked.connect(self._removal_2020_delete_button_clicked)
        ui.removal_2020_table.cellDoubleClicked.connect(self._removal_2020_cell_double_clicked)

    def _last_name_text_changed(self, text: str):
        self._refresh_title()

    def _first_name_text_changed(self, text: str):
        self._refresh_title()

    def _refresh_title(self):
        title: str = self.ui.last_name.text()
        title = f"{title}, {self.ui.first_name.text()}" if self.ui.first_name.text() != '' else title
        title = f"{title}, {self.ui.e4.text()}" if self.ui.e4.text() != '' else title

        self.ui.setWindowTitle(title)

    def _e4_text_changed(self, text: str):
        if self.ui.e4.hasAcceptableInput():
            enabled = self.ui.e4.text() == ""
            self.ui.e4.setEnabled(enabled)
            self.ui.e4_generate.setEnabled(enabled)
            self._refresh_title()

    def _e4_generate_clicked(self):
        id_value: str = generate_id()
        self.ui.e4.setText(id_value)

    def _e6_button_clicked(self, button: QAbstractButton):
        self.ui.e38.setEnabled(button.text() == 'Female')

    def _e7_button_clicked(self, button: QAbstractButton):
        self.ui.e7_required.setVisible(self.ui.e7.checkedButton() is None)

    def _e8_button_clicked(self, button: QAbstractButton):
        required = button.text() == 'Yes' and len(self.ui.e9.selectedIndexes()) == 0
        self.ui.e8_required.setVisible(self.ui.e8.checkedButton() is None)
        self.ui.e9_required.setVisible(required)

    def _e9_set_up(self):
        """sets the 'checked' status of the selected tribes"""
        # TODO: figure out how to set the checked status of the tribes
        ...

    def _e9_item_clicked(self, item: QListWidgetItem):
        self.ui.e9_required.setVisible(len(self.ui.e9.selectedIndexes()) == 0)

    def _e10_button_clicked(self, button: QAbstractButton):
        required = button.text() == 'Yes'
        self.ui.e10_required.setVisible(self.ui.e10.checkedButton() is None)
        self.ui.e11_required.setVisible(required and (self.ui.e11.text() is None or self.ui.e11.text() == ''))
        self.ui.e12_required.setVisible(required and self.ui.e12.checkedButton() is None)

    def _e11_text_changed(self, text: str):
        required = text is None or text == ''
        self.ui.e11_required.setVisible(required)

    def _e12_button_clicked(self, button: QAbstractButton):
        required = button.text() != 'Yes' and button.text() != 'No'
        self.ui.e12_required.setVisible(required)

    def _funding_button_clicked(self, button: QAbstractButton):
        enabled: bool = button.text() == 'No'
        for btn in self.ui.e7.buttons():
            btn.setEnabled(enabled)
        self.ui.e7_required.setVisible(enabled and self.ui.e7.checkedButton() is None)
        for btn in self.ui.e8.buttons():
            btn.setEnabled(enabled)
        self.ui.e8_required.setVisible(enabled and self.ui.e8.checkedButton() is None)
        self.ui.e9.setEnabled(enabled)
        self.ui.e9_required.setVisible(enabled and len(self.ui.e9.selectedItems()) == 0)
        for btn in self.ui.e10.buttons():
            btn.setEnabled(enabled)
        self.ui.e10_required.setVisible(enabled and self.ui.e10.checkedButton() is None)
        self.ui.e11.setEnabled(enabled)
        self.ui.e11_required.setVisible(enabled and (self.ui.e11.text() is None or self.ui.e11.text() == ''))
        for btn in self.ui.e12.buttons():
            btn.setEnabled(enabled)
        self.ui.e12_required.setVisible(enabled and self.ui.e12.checkedButton() is None)

    def _e19_toggled(self, checked: bool):
        # If E19 is checked, E13, E14, E15, E16, E17, E18, E20 should be unchecked and disabled.
        self.ui.e13.setEnabled(not checked)
        self.ui.e14.setEnabled(not checked)
        self.ui.e15.setEnabled(not checked)
        self.ui.e16.setEnabled(not checked)
        self.ui.e17.setEnabled(not checked)
        self.ui.e18.setEnabled(not checked)
        self.ui.e20.setEnabled(not checked)
        if checked:
            self.ui.e13.setChecked(False)
            self.ui.e14.setChecked(False)
            self.ui.e15.setChecked(False)
            self.ui.e16.setChecked(False)
            self.ui.e17.setChecked(False)
            self.ui.e18.setChecked(False)
            self.ui.e20.setChecked(False)
            self.e41 = 7
            self.e44 = 7
        else:
            self.e41 = 1 if self.ui.e42.text() != "" else 0
            self.e44 = 1 if self.ui.e45.text() != "" else 0
        self._e43_error_refresh()

    def _e20_toggled(self, checked: bool):
        # If E20 is checked, E13, E14, E15, E16, E17, E18, E19 should be unchecked and disabled.
        self.ui.e13.setEnabled(not checked)
        self.ui.e14.setEnabled(not checked)
        self.ui.e15.setEnabled(not checked)
        self.ui.e16.setEnabled(not checked)
        self.ui.e17.setEnabled(not checked)
        self.ui.e18.setEnabled(not checked)
        self.ui.e19.setEnabled(not checked)
        if checked:
            self.ui.e13.setChecked(False)
            self.ui.e14.setChecked(False)
            self.ui.e15.setChecked(False)
            self.ui.e16.setChecked(False)
            self.ui.e17.setChecked(False)
            self.ui.e18.setChecked(False)
            self.ui.e19.setChecked(False)

    def _e23_current_index_changed(self, index: int):
        self.ui.e24.setEnabled(index == 1)
        self.ui.e25.setEnabled(index == 1)
        self.ui.e26.setEnabled(index == 1)
        self.ui.e27.setEnabled(index == 1)
        self.ui.e28.setEnabled(index == 1)
        self.ui.e29.setEnabled(index == 1)
        self.ui.e30.setEnabled(index == 1)
        self.ui.e31.setEnabled(index == 1)
        self.ui.e32.setEnabled(index == 1)
        self.ui.e33.setEnabled(index == 1)
        self.ui.e34.setEnabled(index == 1)
        self._e24_error_refresh()

    def _e24_error_refresh(self, *args):
        if self.ui.e23.currentIndex() == 1 and \
                (self.ui.e24.isEnabled() and self.ui.e24.currentIndex() <= 0) and \
                (self.ui.e25.isEnabled() and self.ui.e25.currentIndex() <= 0) and \
                (self.ui.e26.isEnabled() and self.ui.e26.currentIndex() <= 0) and \
                (self.ui.e27.isEnabled() and self.ui.e27.currentIndex() <= 0) and \
                (self.ui.e28.isEnabled() and self.ui.e28.currentIndex() <= 0) and \
                (self.ui.e29.isEnabled() and self.ui.e29.currentIndex() <= 0) and \
                (self.ui.e30.isEnabled() and self.ui.e30.currentIndex() <= 0) and \
                (self.ui.e31.isEnabled() and self.ui.e31.currentIndex() <= 0) and \
                (self.ui.e32.isEnabled() and self.ui.e32.currentIndex() <= 0) and \
                (self.ui.e33.isEnabled() and self.ui.e33.currentIndex() <= 0) and \
                (self.ui.e34.isEnabled() and self.ui.e34.currentIndex() <= 0):
            self.ui.e24_error.setText(self.ERROR_TEMPLATE.substitute(message=self.E24_ERROR_MESSAGE))
        else:
            self.ui.e24_error.setText('')

    def _e42_text_changed(self, text: str):
        self.e41 = 1 if text != "" else 0
        self._e43_error_refresh()

    def _e43_error_refresh(self):
        # adoption_in_another_country_is_required_when_prior_adoption_date_is_entered (and the child is not abandoned)
        if not self.ui.e19.isChecked() and self.ui.e42.text() != "" and self.ui.e43.currentIndex() == -1:
            self.ui.e43_error.setText(self.ERROR_TEMPLATE.substitute(message=self.E43_ERROR_MESSAGE))
        else:
            self.ui.e43_error.setText("")

    def _e45_text_changed(self, text: str):
        self.e44 = 1 if text != "" else 0

    def _set_state_e57(self):
        visible: bool = coalesce(self.ui.e57.text(), 0) > coalesce(self.ui.e56.text(), 0)
        if visible:
            self.ui.e57_error.setText(self.ERROR_TEMPLATE.substitute(message=self.E57_ERROR_MESSAGE))
        else:
            self.ui.e57_error.setText("")
        self.ui.e57_error.setVisible(visible)

    def _second_parents_set_up(self):
        """inject data into the e64/e66/e68 table"""
        ...

    # ===== Removals ==========================================================

    def _removal_set_up(self, removals: list, table: QTableWidget):
        table.clearContents()
        for obj in removals:
            self._add_removal_row(obj, table)

    def _add_removal_row(self, obj, table: QTableWidget) -> None:
        row: int = table.rowCount()
        table.insertRow(row)
        self._replace_removal_row(row, obj, table)

    def _replace_removal_row(self, row: int, obj, table: QTableWidget):
        table.setItem(row, 0, QTableWidgetItem(str(obj.e69)))
        table.setItem(row, 1, QTableWidgetItem(str(obj.e153)))
        table.setItem(row, 2, QTableWidgetItem(
            self.E155_MESSAGES[obj.e155] if obj.e155 in self.E155_MESSAGES else ''))

    # ===== Removal1993 =======================================================

    def _removals1993_set_up(self):
        self._removal_set_up(self.removals1993, self.ui.removal_1993_table)

    def _add_removal_1993_row(self, obj: Removal1993):
        self._add_removal_row(obj, self.ui.removal_1993_table)

    def _replace_removal_1993_row(self, row: int, obj: Removal1993):
        self._replace_removal_row(row, obj, self.ui.removal_1993_table)

    def _removal_1993_add_button_clicked(self):
        removal1993_dialog = Removal1993Dialog()
        obj = Removal1993(ooh=self.obj.id)
        removal1993_dialog.populate(obj)
        if removal1993_dialog.exec():
            self.removals1993.append(obj)
            self._add_removal_1993_row(obj)

    def _removal_1993_edit_button_clicked(self):
        current_row = self.ui.removal_1993_table.currentRow()
        if current_row >= 0:
            removal1993_dialog = Removal1993Dialog()
            obj = self.obj.removals1993[current_row]
            removal1993_dialog.populate(obj)
            if removal1993_dialog.exec():
                self._replace_removal_1993_row(current_row, obj)

    def _removal_1993_cell_double_clicked(self, row: int, col: int):
        self._removal_1993_edit_button_clicked()

    def _removal_1993_delete_button_clicked(self):
        current_row = self.ui.removal_1993_table.currentRow()
        if current_row >= 0:
            if delete_confirmation_dialog(self):
                current_row = self.ui.removal_1993_table.currentRow()
                self.ui.removal_1993_table.removeRow(current_row)
                del self.removals1993[current_row]

    def _removal_1993_cell_activated(self, row: int, column: int):
        self._set_removal_1993_button_status(row >= 0 and column >= 0)

    def _set_removal_1993_button_status(self, is_enabled: bool):
        self.ui.removal_1993_edit_button.setEnabled(is_enabled)
        self.ui.removal_1993_delete_button.setEnabled(is_enabled)

    # ===== Removal2020 =======================================================

    def _removals2020_set_up(self):
        self._removal_set_up(self.removals2020, self.ui.removal_2020_table)

    def _add_removal_2020_row(self, obj: Removal2020):
        self._add_removal_row(obj, self.ui.removal_2020_table)

    def _replace_removal_2020_row(self, row: int, obj: Removal2020):
        self._replace_removal_row(row, obj, self.ui.removal_2020_table)

    def _removal_2020_add_button_clicked(self):
        obj = Removal2020(ooh=self.obj.id, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                          permanency_hearings=[], case_worker_visits=[])
        removal2020_dialog = Removal2020Dialog()
        removal2020_dialog.populate(obj)
        if removal2020_dialog.exec():
            self.removals2020.append(obj)
            self._add_removal_row(obj, self.ui.removal_2020_table)

    def _removal_2020_edit_button_clicked(self):
        current_row = self.ui.removal_2020_table.currentRow()
        if current_row >= 0:
            removal2020_dialog = Removal2020Dialog()
            obj = self.obj.removals2020[current_row]
            removal2020_dialog.populate(obj)
            if removal2020_dialog.exec():
                self._replace_removal_2020_row(current_row, obj)

    def _removal_2020_cell_double_clicked(self, row: int, col: int):
        self._removal_2020_edit_button_clicked()

    def _removal_2020_delete_button_clicked(self):
        current_row = self.ui.removal_2020_table.currentRow()
        if current_row >= 0:
            if delete_confirmation_dialog(self):
                current_row = self.ui.removal_2020_table.currentRow()
                self.ui.removal_2020_table.removeRow(current_row)
                del self.removals2020[current_row]

    def _removal_2020_cell_activated(self, row: int, column: int):
        self._set_removal_2020_button_status(row >= 0 and column >= 0)

    def _set_removal_2020_button_status(self, is_enabled: bool):
        self.ui.removal_2020_edit_button.setEnabled(is_enabled)
        self.ui.removal_2020_delete_button.setEnabled(is_enabled)

    # ===== Parent2 ===========================================================

    def _parent2_add_button_clicked(self):
        parent2dialog = Parent2Dialog()
        obj: SecondParent = SecondParent()
        parent2dialog.populate(obj)
        if parent2dialog.exec():
            self.second_parents.append(obj)
            row: int = self.ui.parent2tpr.rowCount()
            self.ui.parent2tpr.insertRow(row)
            self.ui.parent2tpr.setItem(row, 0, QTableWidgetItem(str(obj.e64)))
            self.ui.parent2tpr.setItem(row, 1, QTableWidgetItem(str(obj.e66)))
            self.ui.parent2tpr.setItem(row, 2, QTableWidgetItem(str(obj.e68)))

    def _parent2_edit_button_clicked(self):
        parent2dialog = Parent2Dialog()
        row: int = self.ui.parent2tpr.currentRow()
        obj: SecondParent = self.second_parents[row]
        parent2dialog.populate(obj)
        if parent2dialog.exec():
            self.ui.parent2tpr.setItem(row, 0, QTableWidgetItem(str(obj.e64)))
            self.ui.parent2tpr.setItem(row, 1, QTableWidgetItem(str(obj.e66)))
            self.ui.parent2tpr.setItem(row, 2, QTableWidgetItem(str(obj.e68)))

    def _parent2tpr_cell_double_clicked(self, row: int, col: int):
        self._parent2_edit_button_clicked()

    # ==================================================================================================================

    def _validate(self) -> bool:
        """validates the form by iterating over the validation rules, return true if the error message list is empty"""
        # TODO: add validation logic
        return True

    def _from_obj(self):
        ui = self.ui
        obj = self.obj
        ui.first_name.setText(obj.child.first_name)
        ui.last_name.setText(obj.child.last_name)
        self._set_int_field(ui.e4, obj.child.e4)
        self._set_date_field(ui.e5, obj.child.e5)
        self._set_radio_button(ui.e6, obj.child.e6)
        self._set_radio_button(ui.e7, obj.e7)
        self._set_radio_button(ui.e8, obj.e8)
        self._set_radio_button(ui.funding, obj.funding)
        self._set_radio_button(ui.e10, obj.e10)
        self._set_int_field(ui.e11, obj.e11)
        self._set_radio_button(ui.e12, obj.e12)
        ui.e13.setChecked(obj.child.e13 == 1)
        ui.e14.setChecked(obj.child.e14 == 1)
        ui.e15.setChecked(obj.child.e15 == 1)
        ui.e16.setChecked(obj.child.e16 == 1)
        ui.e17.setChecked(obj.child.e17 == 1)
        ui.e18.setChecked(obj.child.e18 == 1)
        ui.e19.setChecked(obj.child.e19 == 1)
        ui.e20.setChecked(obj.child.e20 == 1)
        self._set_combobox_selection(ui.e21, obj.child.e21, {0: 0, 1: 1, 7: 2, 8: 3, 9: 4})
        self._set_radio_button(ui.e22, obj.e22)
        self._set_combobox_selection(ui.e23, obj.e23)
        self._set_combobox_selection(ui.e24, obj.e24)
        self._set_combobox_selection(ui.e25, obj.e25)
        self._set_combobox_selection(ui.e26, obj.e26)
        self._set_combobox_selection(ui.e27, obj.e27)
        self._set_combobox_selection(ui.e28, obj.e28)
        self._set_combobox_selection(ui.e29, obj.e29)
        self._set_combobox_selection(ui.e30, obj.e30)
        self._set_combobox_selection(ui.e31, obj.e31)
        self._set_combobox_selection(ui.e32, obj.e32)
        self._set_combobox_selection(ui.e33, obj.e33)
        self._set_combobox_selection(ui.e34, obj.e34)
        self._set_combobox_selection(ui.e35, obj.e35)
        self._set_combobox_selection(ui.e36, obj.e36)
        self._set_combobox_selection(ui.e37, obj.e37)
        self._set_combobox_selection(ui.e38, obj.e38)
        self._set_combobox_selection(ui.e39, obj.e39)
        ui.e47.setChecked(obj.e47 == 1)
        ui.e48.setChecked(obj.e48 == 1)
        ui.e49.setChecked(obj.e49 == 1)
        ui.e50.setChecked(obj.e50 == 1)
        ui.e51.setChecked(obj.e51 == 1)
        ui.e52.setChecked(obj.e52 == 1)
        ui.e53.setChecked(obj.e53 == 1)
        ui.e54.setChecked(obj.e54 == 1)
        self.tribes = obj.tribes
        self._e9_set_up()
        self.second_parents = obj.second_parents
        self._second_parents_set_up()
        self.removals1993 = obj.removals1993
        self._removals1993_set_up()
        self.removals2020 = obj.removals2020
        self._removals2020_set_up()

    # def _button_map(self, button: QButtonGroup, mapping: dict):
    #     text: str = button.checkedButton().text() if button.checkedButton() is not None else None
    #     return mapping[text] if text is not None else None

    # def _to_int(self, text: str) -> int | None:
    #     try:
    #         return int(text)
    #     except ValueError:
    #         return None

    def _to_obj(self):
        def e21_mapping(value: int) -> int:
            if value is None or (value < 0 or value > 9):
                return -1
            return [0, 1, 7, 8, 9][value]

        obj = self.obj
        ui = self.ui
        obj.child.first_name = ui.first_name.text()
        obj.child.last_name = ui.last_name.text()
        obj.child.e4 = self._get_int_field(ui.e4)
        obj.child.e5 = self._get_int_field(ui.e5)
        obj.child.e6 = self._get_radio_button(ui.e6)
        obj.child.e7 = self._get_radio_button(ui.e7)
        obj.child.e8 = self._get_radio_button(ui.e7)
        # obj.child.e9 = ??? # FIXME: need to serialize E9 somehow
        obj.funding = self._get_radio_button(ui.funding)
        obj.child.e10 = self._get_radio_button(ui.e10)
        obj.child.e11 = self._get_int_field(ui.e11)
        obj.child.e12 = self._get_radio_button(ui.e12)
        obj.child.e13 = 1 if ui.e13.isChecked() else 0
        obj.child.e14 = 1 if ui.e14.isChecked() else 0
        obj.child.e15 = 1 if ui.e15.isChecked() else 0
        obj.child.e16 = 1 if ui.e16.isChecked() else 0
        obj.child.e17 = 1 if ui.e17.isChecked() else 0
        obj.child.e18 = 1 if ui.e18.isChecked() else 0
        obj.child.e19 = 1 if ui.e19.isChecked() else 0
        obj.child.e20 = 1 if ui.e20.isChecked() else 0
        obj.child.e21 = self._get_combobox_selection(ui.e21, {0: 0, 1: 1, 2: 7, 3: 8, 4: 9})
        obj.e22 = self._get_radio_button(ui.e22)
        obj.e23 = self._get_combobox_selection(ui.e23)
        obj.e24 = self._get_combobox_selection(ui.e24)
        obj.e25 = self._get_combobox_selection(ui.e25)
        obj.e26 = self._get_combobox_selection(ui.e26)
        obj.e27 = self._get_combobox_selection(ui.e27)
        obj.e28 = self._get_combobox_selection(ui.e28)
        obj.e29 = self._get_combobox_selection(ui.e29)
        obj.e30 = self._get_combobox_selection(ui.e30)
        obj.e31 = self._get_combobox_selection(ui.e31)
        obj.e32 = self._get_combobox_selection(ui.e32)
        obj.e33 = self._get_combobox_selection(ui.e33)
        obj.e34 = self._get_combobox_selection(ui.e34)
        obj.e35 = self._get_combobox_selection(ui.e35)
        obj.e36 = self._get_combobox_selection(ui.e36)
        obj.e37 = self._get_combobox_selection(ui.e37)
        obj.e38 = self._get_combobox_selection(ui.e38) if ui.e38.isEnabled() else None
        obj.e39 = self._get_combobox_selection(ui.e39)
        # TODO: obj.e40 - Indicate Yes = 1 if the child is placed together at any point during the report period.
        #   so... Computed at time of export; for each placement occuring within the reporting period, result is Yes
        #   if any e40 element from the placement record contains a Yes. So that means that e40 needs to be moved into
        #   the placement table.
        # E40 has been moved to the living arrangements form
        # obj.e40 = self._button_map(ui.e40, ChildModelMappings.YES_NO_NA)

        # TODO: E41: Not a field on the screen:
        #   If no date is entered on E42 = 0-No
        #   If a date is entered on E42 = 1-Yes
        #   If Element E19 is yes and no date is entered on E42  = 7-Abandoned
        # obj.e41 = self._button_map(ui.e41, ChildModelMappings.YES_NO_ABANDONED)
        obj.e42 = self._get_int_field(ui.e42)
        obj.e43 = self._get_radio_button(ui.e43)

        # TODO: E44 Not a field on the screen:
        #   If no date is entered on E45 = 0-No
        #   If a date is entered on E45 = 1-Yes
        #   If Element E19 is a yes and no date is entered on E45  = 7-Abandoned
        # obj.e44 = self._button_map(ui.e44, ChildModelMappings.YES_NO_ABANDONED)
        obj.e45 = self._get_int_field(ui.e45)
        obj.e46 = self._get_combobox_selection(ui.e46)
        obj.e47 = 1 if ui.e47.isChecked() else 0
        obj.e48 = 1 if ui.e48.isChecked() else 0
        obj.e49 = 1 if ui.e49.isChecked() else 0
        obj.e50 = 1 if ui.e50.isChecked() else 0
        obj.e51 = 1 if ui.e51.isChecked() else 0
        obj.e52 = 1 if ui.e52.isChecked() else 0
        obj.e53 = 1 if ui.e53.isChecked() else 0
        obj.e54 = 1 if ui.e54.isChecked() else 0
        obj.e55 = self._get_radio_button(ui.e55)
        obj.e56 = self._get_int_field(ui.e56)
        obj.e57 = self._get_int_field(ui.e57)
        # E58 has been moved to the living arrangements form
        # obj.e58 = self._to_int(ui.e58.text())
        obj.e59 = self._get_int_field(ui.e59)
        obj.e60 = self._get_int_field(ui.e60)
        obj.e61 = self._get_radio_button(ui.e61)
        obj.e62 = self._get_radio_button(ui.e62)
        obj.e63 = self._get_radio_button(ui.e63)
        obj.e65 = self._get_int_field(ui.e65)
        obj.e67 = self._get_int_field(ui.e67)
        obj.e107 = self._get_radio_button(ui.e107)
        obj.e108 = self._get_int_field(ui.e108)
        obj.e109 = self._get_radio_button(ui.e109)
        obj.e110 = self._get_radio_button(ui.e110)
        obj.e111 = self._get_int_field(ui.e111)
        obj.tribes = self.tribes  # e9
        obj.second_parents = self.second_parents  # e64, e66, e68
        obj.removals1993 = self.removals1993  # e69, e153, e155
        obj.removals2020 = self.removals2020  # e3, e69-e111, e153-e186
