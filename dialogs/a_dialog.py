from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QWidget

from dialogs import BaseDialog
from utils import generate_id


class ADialog(BaseDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui: QWidget = self.load_ui('ui_adoption_subsidy.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        self.context_id: int = None
        self._child_name: str = ""

    def _wire_ui(self):
        ui = self.ui
        self._init_radio_mf(ui, 'e6')
        self._init_radio(ui, 'a15', {'a': 1, 'g': 2})
        self._init_radio(ui, 'a19', {'1': 1, '2': 2, '3': 3})

        ui.form_action.accepted.connect(self.accept)
        ui.form_action.rejected.connect(self.reject)

        ui.last_name.textChanged.connect(self._last_name_text_changed)
        ui.first_name.textChanged.connect(self._first_name_text_changed)

        ui.e4.textChanged.connect(self._e4_text_changed)
        ui.e4.setValidator(QRegularExpressionValidator(QRegularExpression(r'[0-9a-zA-Z]{12}')))
        ui.e4_generate.clicked.connect(self._e4_generate_clicked)

    def _last_name_text_changed(self, text: str):
        self.child_name = f"{self.last_name}{', ' if self.last_name and self.first_name else ''}{self.first_name}"

    def _first_name_text_changed(self, text: str):
        self.child_name = f"{self.last_name}{', ' if self.last_name and self.first_name else ''}{self.first_name}"

    def clear(self):
        super().clear()
        self.child_name = ""
        self.id = None
        self.context_id = None

    # =========================================================================

    @property
    def child_name(self) -> str:
        return self._child_name

    @child_name.setter
    def child_name(self, v: str) -> None:
        self._child_name = v
        if v:
            self.setWindowTitle(f"{v}{' : ' if self.e4 else ''}{self.e4}")
        else:
            self.setWindowTitle('')

    def _e4_text_changed(self, text: str):
        if self.ui.e4.hasAcceptableInput():
            enabled = self.ui.e4.text() == ""
            self.ui.e4.setEnabled(enabled)
            self.ui.e4_generate.setEnabled(enabled)

    def _e4_generate_clicked(self):
        id_value: str = generate_id()
        self.ui.e4.setText(id_value)

    # =========================================================================

    @property
    def last_name(self) -> str:
        return self.ui.last_name.text()

    @last_name.setter
    def last_name(self, v: str) -> None:
        self.ui.last_name.setText(v)

    @property
    def first_name(self) -> str:
        return self.ui.first_name.text()

    @first_name.setter
    def first_name(self, v: str) -> None:
        self.ui.first_name.setText(v)

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
    def e20(self) -> int:
        return 1 if self.ui.e20.isChecked() else 0

    @e20.setter
    def e20(self, v: int) -> None:
        self.ui.e20.setChecked(v == 1)

    @property
    def e21(self) -> int:
        return self._get_combobox_selection(self.ui.e21, {0: 0, 1: 1, 2: 7, 3: 8, 4: 9})

    @e21.setter
    def e21(self, v: int):
        self._set_combobox_selection(self.ui.e21, v, {0: 0, 1: 1, 7: 2, 8: 3, 9: 4})

    @property
    def a15(self) -> int:
        return self._get_radio_button(self.ui.a15)

    @a15.setter
    def a15(self, v: int) -> None:
        self._set_radio_button(self.ui.a15, v)

    @property
    def a16(self) -> int:
        return self._get_int_field(self.ui.a16)

    @a16.setter
    def a16(self, v: int):
        self._set_int_field(self.ui.a16, v)

    @property
    def a17(self) -> int:
        return self._get_int_field(self.ui.a17)

    @a17.setter
    def a17(self, v: int) -> None:
        self._set_int_field(self.ui.a17, v)

    @property
    def a18(self) -> int:
        return self._get_int_field(self.ui.a18)

    @a18.setter
    def a18(self, v: int) -> None:
        self._set_int_field(self.ui.a18, v)

    @property
    def a19(self) -> int:
        self._get_radio_button(self.ui.a19)

    @a19.setter
    def a19(self, v: int) -> None:
        self._set_radio_button(self.ui.a19, v)
