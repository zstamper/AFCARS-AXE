# -*- coding: utf-8 -*-
from typing import Optional, Callable, Any

# from .childform import Ui_ChildForm
from PySide6.QtCore import (QRegularExpression)
from PySide6.QtGui import (QRegularExpressionValidator)
from PySide6.QtWidgets import (QAbstractButton, QWidget, QListWidgetItem, QTableWidgetItem)

from model import SecondParent, Removal1993, Removal2020, RecognizedTribe, ARecord
from model.models import Tribe
from utils import generate_id
from . import BaseDialog


class OOHDialog(BaseDialog):
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

        self.a: ARecord | None = None

        # Virtual elements:

        # back-end stores for our virtual properties
        self._epa_tribes: list[Tribe] = []
        self._recognized_tribes: list[RecognizedTribe] = []
        self._second_parents: list[SecondParent] = []
        self._removals1993: list[Removal1993] = []
        self._removals2020: list[Removal2020] = []
        self._child_name: str = ""

        # Callbacks
        self.on_add_tribe_clicked: Optional[Callable] = None
        self.on_remove_tribe_clicked: Optional[Callable] = None
        self.on_add_second_parent: Optional[Callable] = None
        self.on_edit_second_parent: Optional[Callable] = None
        self.on_add_removal1993_clicked: Optional[Callable] = None
        self.on_edit_removal1993_clicked: Optional[Callable] = None
        self.on_delete_removal1993_clicked: Optional[Callable] = None
        self.on_add_removal2020_clicked: Optional[Callable] = None
        self.on_edit_removal2020_clicked: Optional[Callable] = None
        self.on_delete_removal2020_clicked: Optional[Callable] = None
        self.on_tab_changed: Optional[Callable] = None
        self.on_validate_clicked: Optional[Callable] = None
        self.on_save: Optional[Callable] = None
        self.on_close: Optional[Callable] = None

        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())

    def clear(self, exclude: list[str] = None) -> None:
        super().clear(exclude=['epa_tribes', ])
        self.setWindowTitle("")
        self.current_tab = 0

    # ==================================================================================================================

    def set_epa_ids(self, tribe_iterator: iter) -> None:
        self.tribes = tribe_iterator
        for state, tribes in tribe_iterator:
            for tribe in tribes:
                item = QListWidgetItem(f"{state} - {tribe.tribe}")
                self.ui.tribes.addItem(QListWidgetItem(item))

    def enable_icwa(self, is_enabled: bool) -> None:
        self.ui.tabWidget.tabBar().setTabEnabled(1, is_enabled)

    # ==================================================================================================================

    # noinspection PyPropertyAccess
    def _wire_ui(self) -> None:
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
        self._init_radio_yn(ui, 'e106')
        self._init_radio_yn(ui, 'e109')

        "Set-up business rules implemented at UI level"
        ui.save_button.clicked.connect(self.do_save_clicked)
        ui.close_button.clicked.connect(self.do_close_clicked)

        ui.last_name.textChanged.connect(self._last_name_text_changed)
        ui.first_name.textChanged.connect(self._first_name_text_changed)

        ui.funding.buttonClicked.connect(self._funding_button_clicked)

        ui.e4.textChanged.connect(self._e4_text_changed)
        ui.e4.setValidator(QRegularExpressionValidator(QRegularExpression(r'[0-9a-zA-Z]{12}')))
        ui.e4_generate.clicked.connect(self._e4_generate_clicked)

        ui.e6.buttonClicked.connect(self._e6_button_clicked)
        # ui.e7.buttonClicked.connect(self._e7_button_clicked)
        # ui.e8.buttonClicked.connect(self._e8_button_clicked)

        ui.add_tribe_button.clicked.connect(self._on_add_tribe_clicked)
        ui.remove_tribe_button.clicked.connect(self._on_remove_tribe_clicked)

        ui.e19.toggled.connect(self._e19_toggled)
        ui.e20.toggled.connect(self._e20_toggled)

        ui.e23.currentIndexChanged.connect(self._e23_current_index_changed)

        ui.parent2_add_button.clicked.connect(self._on_add_second_parent)
        ui.parent2_edit_button.clicked.connect(self._on_edit_second_parent)
        ui.parent2tpr.cellDoubleClicked.connect(self._on_edit_second_parent)

        ui.removal_1993_add_button.clicked.connect(self._on_add_removal1993_clicked)
        ui.removal_1993_edit_button.clicked.connect(self._on_edit_removal1993_clicked)
        ui.removal_1993_delete_button.clicked.connect(self._on_delete_removal1993_clicked)
        ui.removal_1993_table.cellDoubleClicked.connect(self._on_edit_removal1993_clicked)
        ui.removal_2020_add_button.clicked.connect(self._on_add_removal2020_clicked)
        ui.removal_2020_edit_button.clicked.connect(self._on_edit_removal2020_clicked)
        ui.removal_2020_delete_button.clicked.connect(self._on_delete_removal2020_clicked)
        ui.removal_2020_table.cellDoubleClicked.connect(self._on_edit_removal2020_clicked)

        ui.tabWidget.currentChanged.connect(self._on_tab_changed)
        ui.validate_button.clicked.connect(self.do_validate_clicked)

    # ==================================================================================================================
    #
    #                                                   PROPERTIES
    #
    # ==================================================================================================================

    def _on_add_second_parent(self) -> Any:
        return self.on_add_second_parent() if self.on_add_second_parent else None

    def _on_edit_second_parent(self) -> Any:
        return self.on_edit_second_parent() if self.on_edit_second_parent else None

    def _on_add_tribe_clicked(self) -> Any:
        return self.on_add_tribe_clicked() if self.on_add_tribe_clicked else None

    def _on_remove_tribe_clicked(self) -> Any:
        return self.on_remove_tribe_clicked() if self.on_remove_tribe_clicked else None

    def _on_add_removal1993_clicked(self) -> Any:
        return self.on_add_removal1993_clicked() if self.on_add_removal1993_clicked else None

    def _on_edit_removal1993_clicked(self) -> Any:
        return self.on_edit_removal1993_clicked() if self.on_edit_removal1993_clicked else None

    def _on_delete_removal1993_clicked(self) -> Any:
        return self.on_delete_removal1993_clicked() if self.on_delete_removal1993_clicked else None

    def _on_add_removal2020_clicked(self) -> Any:
        return self.on_add_removal2020_clicked() if self.on_add_removal2020_clicked else None

    def _on_edit_removal2020_clicked(self) -> Any:
        return self.on_edit_removal2020_clicked() if self.on_edit_removal2020_clicked else None

    def _on_delete_removal2020_clicked(self) -> Any:
        return self.on_delete_removal2020_clicked() if self.on_delete_removal2020_clicked else None

    def _on_tab_changed(self, new_tab: int) -> Any:
        return self.on_tab_changed(new_tab) if self.on_tab_changed else None

    def do_validate_clicked(self) -> Any:
        return self.on_validate_clicked() if self.on_validate_clicked else None

    def do_save_clicked(self) -> Any:
        return self.on_save() if self.on_save else None

    def do_close_clicked(self) -> Any:
        if self.on_close:
            if self.on_close():
                self.close()

    def tab_label(self, tab: int) -> str:
        return self.ui.tabWidget.tabText(tab)

    def set_tab_label(self, tab: int, label: str) -> None:
        self.ui.tabWidget.setTabText(tab, label)

    @property
    def current_tab(self) -> int:
        return self.ui.tabWidget.currentIndex()

    @current_tab.setter
    def current_tab(self, new_tab: int) -> None:
        self.ui.tabWidget.setCurrentIndex(new_tab)

    def _last_name_text_changed(self, text: str) -> None:
        self.child_name = f"{self.last_name if self.last_name else ''}{', ' if self.last_name and self.first_name else ''}{self.first_name if self.first_name else ''}"

    def _first_name_text_changed(self, text: str) -> None:
        self.child_name = f"{self.last_name if self.last_name else ''}{', ' if self.last_name and self.first_name else ''}{self.first_name if self.first_name else ''}"

    def _refresh_title(self) -> None:
        self.setWindowTitle(f"{self.child_name}{' : ' if self.e4 else ''}{self.e4 if self.e4 else ''}")

    def _e4_text_changed(self, text: str) -> None:
        if self.ui.e4.hasAcceptableInput():
            enabled = self.ui.e4.text() == ""
            self.ui.e4.setEnabled(enabled)
            self.ui.e4_generate.setEnabled(enabled)
            self._refresh_title()

    def _e4_generate_clicked(self) -> None:
        id_value: str = generate_id()
        self.ui.e4.setText(id_value)

    def _e6_button_clicked(self, button: QAbstractButton) -> None:
        self.ui.e38.setEnabled(button.text() == 'Female')

    # def _e7_button_clicked(self, button: QAbstractButton):
    #     self.ui.e7_required.setVisible(self.ui.e7.checkedButton() is None)
    #
    # def _e8_button_clicked(self, button: QAbstractButton):
    #     required = button.text() == 'Yes' and len(self.ui.e9.selectedIndexes()) == 0
    #     self.ui.e8_required.setVisible(self.ui.e8.checkedButton() is None)
    #     self.ui.e9_required.setVisible(required)

    def _e9_set_up(self) -> None:
        """sets the 'checked' status of the selected tribes"""
        # TODO: figure out how to set the checked status of the tribes
        ...

    def _funding_button_clicked(self, button: QAbstractButton) -> None:
        enabled: bool = button.text() == 'No'
        for btn in self.ui.e7.buttons():
            btn.setEnabled(enabled)
        for btn in self.ui.e8.buttons():
            btn.setEnabled(enabled)
        self.ui.tribes.setEnabled(enabled)
        self.ui.epa_tribes.setEnabled(enabled)
        self.ui.add_tribe_button.setEnabled(enabled)
        self.ui.remove_tribe_button.setEnabled(enabled)
        for btn in self.ui.e10.buttons():
            btn.setEnabled(enabled)
        self.ui.e11.setEnabled(enabled)
        for btn in self.ui.e12.buttons():
            btn.setEnabled(enabled)

    def _e19_toggled(self, checked: bool) -> None:
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

    def _e20_toggled(self, checked: bool) -> None:
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

    def _e23_current_index_changed(self, index: int) -> None:
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

    @property
    def child_name(self) -> str:
        return self._child_name

    @child_name.setter
    def child_name(self, v: str) -> None:
        self._child_name = v
        self._refresh_title()

    @property
    def first_name(self):
        return self._get_text_field(self.ui.first_name)

    @first_name.setter
    def first_name(self, v: str) -> None:
        self._set_text_field(self.ui.first_name, v)

    @property
    def last_name(self) -> str:
        return self._get_text_field(self.ui.last_name)

    @last_name.setter
    def last_name(self, v: str) -> None:
        self._set_text_field(self.ui.last_name, v)

    @property
    def e4(self) -> str:
        return self._get_text_field(self.ui.e4)

    @e4.setter
    def e4(self, v: str) -> None:
        self._set_text_field(self.ui.e4, v)

    @property
    def e5(self) -> int | None:
        return self._get_int_field(self.ui.e5)

    @e5.setter
    def e5(self, v: int) -> None:
        self._set_int_field(self.ui.e5, v)

    @property
    def e6(self) -> int:
        return self._get_radio_button(self.ui.e6)

    @e6.setter
    def e6(self, v: int) -> None:
        self._set_radio_button(self.ui.e6, v)

    @property
    def e7(self) -> int:
        return self._get_radio_button(self.ui.e7)

    @e7.setter
    def e7(self, v: int) -> None:
        self._set_radio_button(self.ui.e7, v)

    @property
    def e8(self) -> int:
        return self._get_radio_button(self.ui.e8)

    @e8.setter
    def e8(self, v: int) -> None:
        self._set_radio_button(self.ui.e8, v)

    @property
    def tribes(self) -> list[RecognizedTribe]:
        return self._recognized_tribes

    @tribes.setter
    def tribes(self, v: list[RecognizedTribe]) -> None:
        self._recognized_tribes = v
        self.refresh_tribes()

    def current_tribe_row(self) -> int:
        return self.ui.tribes.currentRow()

    def current_epa_tribe_row(self) -> int:
        return self.ui.epa_tribes.currentRow()

    def refresh_tribes(self) -> None:
        self.ui.tribes.clear()
        lookup = {tribe.id: str(tribe) for tribe in self.epa_tribes}
        for tribe in self.tribes:
            self.ui.tribes.addItem(lookup[tribe.e9])

    @property
    def epa_tribes(self) -> list[Tribe]:
        return self._epa_tribes

    @epa_tribes.setter
    def epa_tribes(self, v: list[Tribe]):
        self._epa_tribes = v
        self.refresh_epa_tribes()

    def refresh_epa_tribes(self):
        self.ui.epa_tribes.clear()
        for tribe in self._epa_tribes:
            self.ui.epa_tribes.addItem(str(tribe))

    @property
    def funding(self) -> int:
        return self._get_radio_button(self.ui.funding)

    @funding.setter
    def funding(self, v: int) -> None:
        self._set_radio_button(self.ui.funding, v)

    @property
    def e10(self) -> int:
        return self._get_radio_button(self.ui.e10)

    @e10.setter
    def e10(self, v: int) -> None:
        self._set_radio_button(self.ui.e10, v)

    @property
    def e11(self) -> int | None:
        return self._get_int_field(self.ui.e11)

    @e11.setter
    def e11(self, v: int) -> None:
        self._set_int_field(self.ui.e11, v)

    @property
    def e12(self) -> int:
        return self._get_radio_button(self.ui.e12)

    @e12.setter
    def e12(self, v: int) -> None:
        self._set_radio_button(self.ui.e12, v)

    @property
    def e13(self) -> int:
        return 1 if self.ui.e13.isChecked() else 0

    @e13.setter
    def e13(self, v: int) -> None:
        self.ui.e13.setChecked(v == 1)

    @property
    def e14(self) -> int:
        return 1 if self.ui.e14.isChecked() else 0

    @e14.setter
    def e14(self, v: int) -> None:
        self.ui.e14.setChecked(v == 1)

    @property
    def e15(self) -> int:
        return 1 if self.ui.e15.isChecked() else 0

    @e15.setter
    def e15(self, v: int) -> None:
        self.ui.e15.setChecked(v == 1)

    @property
    def e16(self) -> int:
        return 1 if self.ui.e16.isChecked() else 0

    @e16.setter
    def e16(self, v: int) -> None:
        self.ui.e16.setChecked(v == 1)

    @property
    def e17(self) -> int:
        return 1 if self.ui.e17.isChecked() else 0

    @e17.setter
    def e17(self, v: int) -> None:
        self.ui.e17.setChecked(v == 1)

    @property
    def e18(self) -> int:
        return 1 if self.ui.e18.isChecked() else 0

    @e18.setter
    def e18(self, v: int) -> None:
        self.ui.e18.setChecked(v == 1)

    @property
    def e19(self) -> int:
        return 1 if self.ui.e19.isChecked() else 0

    @e19.setter
    def e19(self, v: int) -> None:
        self.ui.e19.setChecked(v == 1)

    @property
    def e20(self) -> int | None:
        return 1 if self.ui.e20.isChecked() else 0

    @e20.setter
    def e20(self, v: int) -> None:
        self.ui.e20.setChecked(v == 1)

    @property
    def e21(self) -> int | None:
        return self._get_combobox_selection(self.ui.e21, {0: 0, 1: 1, 2: 7, 3: 8, 4: 9})

    @e21.setter
    def e21(self, v: int):
        self._set_combobox_selection(self.ui.e21, v, {0: 0, 1: 1, 7: 2, 8: 3, 9: 4})

    @property
    def e22(self) -> int | None:
        return self._get_radio_button(self.ui.e22)

    @e22.setter
    def e22(self, v: int) -> None:
        self._set_radio_button(self.ui.e22, v)

    @property
    def e23(self) -> int | None:
        return self._get_combobox_selection(self.ui.e23)

    @e23.setter
    def e23(self, v: int):
        self._set_combobox_selection(self.ui.e23, v)

    @property
    def e24(self) -> int | None:
        return self._get_combobox_selection(self.ui.e24)

    @e24.setter
    def e24(self, v: int):
        self._set_combobox_selection(self.ui.e24, v)

    @property
    def e25(self) -> int | None:
        return self._get_combobox_selection(self.ui.e25)

    @e25.setter
    def e25(self, v: int):
        self._set_combobox_selection(self.ui.e25, v)

    @property
    def e26(self) -> int | None:
        return self._get_combobox_selection(self.ui.e26)

    @e26.setter
    def e26(self, v: int):
        self._set_combobox_selection(self.ui.e26, v)

    @property
    def e27(self) -> int | None:
        return self._get_combobox_selection(self.ui.e27)

    @e27.setter
    def e27(self, v: int):
        self._set_combobox_selection(self.ui.e27, v)

    @property
    def e28(self) -> int | None:
        return self._get_combobox_selection(self.ui.e28)

    @e28.setter
    def e28(self, v: int):
        self._set_combobox_selection(self.ui.e28, v)

    @property
    def e29(self) -> int | None:
        return self._get_combobox_selection(self.ui.e29)

    @e29.setter
    def e29(self, v: int):
        self._set_combobox_selection(self.ui.e29, v)

    @property
    def e30(self) -> int | None:
        return self._get_combobox_selection(self.ui.e30)

    @e30.setter
    def e30(self, v: int):
        self._set_combobox_selection(self.ui.e30, v)

    @property
    def e31(self) -> int | None:
        return self._get_combobox_selection(self.ui.e31)

    @e31.setter
    def e31(self, v: int):
        self._set_combobox_selection(self.ui.e31, v)

    @property
    def e32(self) -> int | None:
        return self._get_combobox_selection(self.ui.e32)

    @e32.setter
    def e32(self, v: int):
        self._set_combobox_selection(self.ui.e32, v)

    @property
    def e33(self) -> int | None:
        return self._get_combobox_selection(self.ui.e33)

    @e33.setter
    def e33(self, v: int):
        self._set_combobox_selection(self.ui.e33, v)

    @property
    def e34(self) -> int | None:
        return self._get_combobox_selection(self.ui.e34)

    @e34.setter
    def e34(self, v: int):
        self._set_combobox_selection(self.ui.e34, v)

    @property
    def e35(self) -> int | None:
        return self._get_combobox_selection(self.ui.e35)

    @e35.setter
    def e35(self, v: int):
        self._set_combobox_selection(self.ui.e35, v)

    @property
    def e36(self) -> int | None:
        return self._get_combobox_selection(self.ui.e36)

    @e36.setter
    def e36(self, v: int):
        self._set_combobox_selection(self.ui.e36, v)

    @property
    def e37(self) -> int | None:
        return self._get_combobox_selection(self.ui.e37)

    @e37.setter
    def e37(self, v: int):
        self._set_combobox_selection(self.ui.e37, v)

    @property
    def e38(self) -> int | None:
        return self._get_combobox_selection(self.ui.e38) if self.ui.e38.isEnabled() else None

    @e38.setter
    def e38(self, v: int):
        self._set_combobox_selection(self.ui.e38, v)

    @property
    def e39(self) -> int | None:
        return self._get_combobox_selection(self.ui.e39)

    @e39.setter
    def e39(self, v: int):
        self._set_combobox_selection(self.ui.e39, v)

    @property
    def e41(self) -> int:
        return \
            7 if self.e19 == 1 and not self.e42 \
                else 0 if not self.e42 \
                else 1

    @e41.setter
    def e41(self, v: int) -> None:
        # deliberately left blank: we need to be able to set the value so that the data flows don't crash, but we really
        # don't care what the value is, since this is a computed field.
        pass

    @property
    def e42(self) -> int | None:
        return self._get_int_field(self.ui.e42)

    @e42.setter
    def e42(self, v: int) -> None:
        self._set_int_field(self.ui.e42, v)

    @property
    def e43(self) -> int | None:
        # FIXME: e43 is currently a combobox
        return self._get_combobox_selection(self.ui.e43)

    @e43.setter
    def e43(self, v: int) -> None:
        self._set_combobox_selection(self.ui.e43, v)

    @property
    def e44(self) -> int:
        return \
            7 if self.e19 == 1 and not self.e45 \
                else 0 if not self.e45 \
                else 1

    @e44.setter
    def e44(self, v: int) -> None:
        # deliberately left blank: we need to be able to set the value so that the data flows don't crash, but we really
        # don't care what the value is, since this is a computed field.
        pass

    @property
    def e45(self) -> int | None:
        return self._get_int_field(self.ui.e45)

    @e45.setter
    def e45(self, v: int) -> None:
        self._set_int_field(self.ui.e45, v)

    @property
    def e46(self) -> int:
        return 1 if (self.e47 == 1 or self.e48 == 1 or self.e49 == 1 or self.e50 == 1 or
                     self.e51 == 1 or self.e52 == 1 or self.e53 == 1 or self.e54 == 1) else 0

    @e46.setter
    def e46(self, v: int) -> None:
        if v == 0:
            self.e47 = 0
            self.e48 = 0
            self.e49 = 0
            self.e50 = 0
            self.e51 = 0
            self.e52 = 0
            self.e53 = 0
            self.e54 = 0

    @property
    def e47(self) -> int:
        return 1 if self.ui.e47.isChecked() else 0

    @e47.setter
    def e47(self, v: int) -> None:
        self.ui.e47.setChecked(v == 1)

    @property
    def e48(self) -> int:
        return 1 if self.ui.e48.isChecked() else 0

    @e48.setter
    def e48(self, v: int) -> None:
        self.ui.e48.setChecked(v == 1)

    @property
    def e49(self) -> int:
        return 1 if self.ui.e49.isChecked() else 0

    @e49.setter
    def e49(self, v: int) -> None:
        self.ui.e49.setChecked(v == 1)

    @property
    def e50(self) -> int:
        return 1 if self.ui.e50.isChecked() else 0

    @e50.setter
    def e50(self, v: int) -> None:
        self.ui.e50.setChecked(v == 1)

    @property
    def e51(self) -> int:
        return 1 if self.ui.e51.isChecked() else 0

    @e51.setter
    def e51(self, v: int) -> None:
        self.ui.e51.setChecked(v == 1)

    @property
    def e52(self) -> int:
        return 1 if self.ui.e52.isChecked() else 0

    @e52.setter
    def e52(self, v: int) -> None:
        self.ui.e52.setChecked(v == 1)

    @property
    def e53(self) -> int:
        return 1 if self.ui.e53.isChecked() else 0

    @e53.setter
    def e53(self, v: int) -> None:
        self.ui.e53.setChecked(v == 1)

    @property
    def e54(self) -> int:
        return 1 if self.ui.e54.isChecked() else 0

    @e54.setter
    def e54(self, v: int) -> None:
        self.ui.e54.setChecked(v == 1)

    @property
    def e55(self) -> int:
        return 1 if self.ui.e55.isChecked() else 0

    @e55.setter
    def e55(self, v: int) -> None:
        self.ui.e55.setChecked(v == 1)

    @property
    def e56(self) -> int | None:
        return self._get_int_field(self.ui.e56)

    @e56.setter
    def e56(self, v: int) -> None:
        self._set_int_field(self.ui.e56, v)

    @property
    def e57(self) -> int | None:
        return self._get_int_field(self.ui.e57)

    @e57.setter
    def e57(self, v: int) -> None:
        self._set_int_field(self.ui.e57, v)

    @property
    def e59(self) -> int | None:
        return self._get_int_field(self.ui.e59)

    @e59.setter
    def e59(self, v: int) -> None:
        self._set_int_field(self.ui.e59, v)

    @property
    def e60(self) -> int | None:
        return self._get_int_field(self.ui.e60)

    @e60.setter
    def e60(self, v: int) -> None:
        self._set_int_field(self.ui.e60, v)

    @property
    def e61(self) -> int:
        return self._get_radio_button(self.ui.e61)

    @e61.setter
    def e61(self, v: int) -> None:
        self._set_radio_button(self.ui.e61, v)

    @property
    def e62(self) -> int:
        return self._get_radio_button(self.ui.e62)

    @e62.setter
    def e62(self, v: int) -> None:
        self._set_radio_button(self.ui.e62, v)

    @property
    def e63(self) -> int:
        return self._get_radio_button(self.ui.e63)

    @e63.setter
    def e63(self, v: int) -> None:
        self._set_radio_button(self.ui.e63, v)

    @property
    def e65(self) -> int | None:
        return self._get_int_field(self.ui.e65)

    @e65.setter
    def e65(self, v: int) -> None:
        self._set_int_field(self.ui.e65, v)

    @property
    def e67(self) -> int | None:
        return self._get_int_field(self.ui.e67)

    @e67.setter
    def e67(self, v: int) -> None:
        self._set_int_field(self.ui.e67, v)

    @property
    def e106(self) -> int:
        return self._get_radio_button(self.ui.e106)

    @e106.setter
    def e106(self, v: int) -> None:
        self._set_radio_button(self.ui.e106, v)

    @property
    def e107(self) -> int:
        return self._get_radio_button(self.ui.e107)

    @e107.setter
    def e107(self, v: int) -> None:
        self._set_radio_button(self.ui.e107, v)

    @property
    def e108(self) -> int | None:
        return self._get_int_field(self.ui.e108)

    @e108.setter
    def e108(self, v: int) -> None:
        self._set_int_field(self.ui.e108, v)

    @property
    def e109(self) -> int:
        return self._get_radio_button(self.ui.e109)

    @e109.setter
    def e109(self, v: int) -> None:
        self._set_radio_button(self.ui.e109, v)

    @property
    def e110(self) -> int:
        return self._get_radio_button(self.ui.e110)

    @e110.setter
    def e110(self, v: int) -> None:
        self._set_radio_button(self.ui.e110, v)

    @property
    def e111(self) -> int | None:
        return self._get_int_field(self.ui.e111)

    @e111.setter
    def e111(self, v: int) -> None:
        self._set_int_field(self.ui.e111, v)

    @property
    def removals1993(self) -> list[Removal1993]:
        return self._removals1993

    @removals1993.setter
    def removals1993(self, data: list[Removal1993]) -> None:
        self._removals1993 = data
        self.refresh_removals1993()

    def refresh_removals1993(self) -> None:
        self.ui.removal_1993_table.clearContents()
        for _ in range(self.ui.removal_1993_table.rowCount()):
            self.ui.removal_1993_table.removeRow(0)
        for data in self._removals1993:
            row: int = self.ui.removal_1993_table.rowCount()
            self.ui.removal_1993_table.insertRow(row)
            self.ui.removal_1993_table.setItem(row, 0, QTableWidgetItem(str(data.e69)))
            self.ui.removal_1993_table.setItem(row, 1, QTableWidgetItem(str(data.e153)))
            self.ui.removal_1993_table.setItem(row, 2, QTableWidgetItem(
                self.E155_MESSAGES[data.e155] if data.e155 in self.E155_MESSAGES else ''))

    def current_removal1993_row(self) -> int:
        return self.ui.removal_1993_table.currentRow()

    @property
    def removals2020(self) -> list[Removal2020]:
        return self._removals2020

    @removals2020.setter
    def removals2020(self, data: list[Removal2020]):
        self._removals2020 = data
        self.refresh_removals2020()

    def refresh_removals2020(self):
        self.ui.removal_2020_table.clearContents()
        for row in range(self.ui.removal_2020_table.rowCount()):
            self.ui.removal_2020_table.removeRow(0)
        for data in self.removals2020:
            row: int = self.ui.removal_2020_table.rowCount()
            self.ui.removal_2020_table.insertRow(row)
            self.ui.removal_2020_table.setItem(row, 0, QTableWidgetItem(str(data.e69)))
            self.ui.removal_2020_table.setItem(row, 1, QTableWidgetItem(str(data.e153)))
            self.ui.removal_2020_table.setItem(row, 2, QTableWidgetItem(
                self.E155_MESSAGES[data.e155] if data.e155 in self.E155_MESSAGES else ''))

    def current_removal2020_row(self) -> int:
        return self.ui.removal_2020_table.currentRow()

    @property
    def second_parents(self) -> list[SecondParent]:
        return self._second_parents

    @second_parents.setter
    def second_parents(self, data: list[SecondParent]) -> None:
        self._second_parents = data
        self.refresh_second_parents()

    def current_second_parents_row(self) -> int:
        return self.ui.parent2tpr.currentRow()

    def refresh_second_parents(self) -> None:
        self.ui.parent2tpr.clearContents()
        for _ in range(self.ui.parent2tpr.rowCount()):
            self.ui.parent2tpr.removeRow(0)
        for row, data in enumerate(self.second_parents):
            if row >= self.ui.parent2tpr.rowCount():
                self.ui.parent2tpr.insertRow(row)
            self.ui.parent2tpr.setItem(row, 0, QTableWidgetItem(str(data.number)))
            self.ui.parent2tpr.setItem(row, 1, QTableWidgetItem(str(data.e64_as_str())))
            self.ui.parent2tpr.setItem(row, 2, QTableWidgetItem(str(data.e66)))
            self.ui.parent2tpr.setItem(row, 3, QTableWidgetItem(str(data.e68)))
            row += 1
        while self.ui.parent2tpr.rowCount() > len(self.second_parents):
            self.ui.parent2tpr.removeRow(self.ui.parent2tpr.rowCount() - 1)
