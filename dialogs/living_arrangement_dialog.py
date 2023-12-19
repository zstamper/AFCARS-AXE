from typing import Optional, Callable

from PySide6.QtWidgets import QWidget

from dialogs import BaseDialog


class LivingArrangementDialog(BaseDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = self.load_ui('ui_living_arrangement.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        self.id: int | None = None
        self.removal_id: int | None = None
        self._child_name: str = ""
        self.on_validate_clicked: Optional[Callable] = None

    def _wire_ui(self) -> None:
        self.setModal(True)
        ui = self.ui

        ui.form_action.accepted.connect(self.accept)
        ui.form_action.rejected.connect(self.reject)

        # assign id numbers to the radio buttons -- can't be done through the UI app
        self._init_radio_ynna(ui, 'e40')
        self._init_radio_ynu(ui, 'e126')
        self._init_radio_ynud(ui, 'e134')
        self._init_radio_mf(ui, 'e135')
        self._init_radio_ynu(ui, 'e137')
        self._init_radio_ynud(ui, 'e145')
        self._init_radio_mf(ui, 'e146')

        self.ui.e121.currentIndexChanged.connect(self._e121_changed)
        self.ui.e123.currentIndexChanged.connect(self._e123_changed)

        self.ui.validate_button.clicked.connect(self.do_validate_button_clicked)

    def _e121_changed(self):
        self.ui.e122.setEnabled(self.e121 not in (1, 4))

    def _e123_changed(self):
        enabled = self.e123 in (1, 2)
        self.ui.e136.setEnabled(enabled)
        self.ui.e146.setEnabled(enabled)
        self.ui.e138.setEnabled(enabled)
        self.ui.e139.setEnabled(enabled)
        self.ui.e140.setEnabled(enabled)
        self.ui.e141.setEnabled(enabled)
        self.ui.e142.setEnabled(enabled)
        self.ui.e143.setEnabled(enabled)
        self.ui.e144.setEnabled(enabled)
        self.ui.e145.setEnabled(enabled)
        self.ui.e137.setEnabled(enabled)

    def _e133_changed(self):
        enabled = self.e133 != 1
        self.ui.e127.setEnabled(enabled)
        self.ui.e128.setEnabled(enabled)
        self.ui.e129.setEnabled(enabled)
        self.ui.e130.setEnabled(enabled)
        self.ui.e131.setEnabled(enabled)
        self.ui.e132.setEnabled(enabled)
        if self.e133 == 1:
            self.e127 = 0
            self.e128 = 0
            self.e129 = 0
            self.e130 = 0
            self.e131 = 0
            self.e132 = 0

    def do_validate_button_clicked(self):
        if self.on_validate_clicked:
            self.on_validate_clicked()

    @property
    def child_name(self) -> str:
        return self._child_name

    @child_name.setter
    def child_name(self, v: str):
        self._child_name = v
        if v:
            self.setWindowTitle(f"Living Arrangement : {v}")
        else:
            self.setWindowTitle("")

    @property
    def e40(self) -> int:
        return self._get_radio_button(self.ui.e40)

    @e40.setter
    def e40(self, v: int) -> None:
        self._set_radio_button(self.ui.e40, v)

    @property
    def e58(self) -> int:
        return self._get_int_field(self.ui.e58)

    @e58.setter
    def e58(self, v: int) -> None:
        self._set_int_field(self.ui.e58, v)

    @property
    def e112(self) -> int:
        return self._get_int_field(self.ui.e112)

    @e112.setter
    def e112(self, v: int) -> None:
        self._set_int_field(self.ui.e112, v)

    @property
    def e113(self) -> int:
        return 1 if self.e120 == 0 else 0

    @e113.setter
    def e113(self, v: int) -> None:
        if v:
            self.e120 = 0

    @property
    def e114(self) -> int:
        return 1 if self.ui.e114.isChecked() else 0

    @e114.setter
    def e114(self, v: int):
        self.ui.e114.setChecked(v == 1)

    @property
    def e115(self) -> int:
        return 1 if self.ui.e115.isChecked() else 0

    @e115.setter
    def e115(self, v: int):
        self.ui.e115.setChecked(v == 1)

    @property
    def e116(self) -> int:
        return 1 if self.ui.e116.isChecked() else 0

    @e116.setter
    def e116(self, v: int):
        self.ui.e116.setChecked(v == 1)

    @property
    def e117(self) -> int:
        return 1 if self.ui.e124.currentText() == 'Relative' else 0

    @e117.setter
    def e117(self, v: int) -> None:
        # e117 is essentially a read-only field; it's derived from e124. defining an empty setter ensures our automation
        # works properly.
        pass

    @property
    def e118(self) -> int:
        return 1 if self.ui.e118.isChecked() else 0

    @e118.setter
    def e118(self, v: int) -> None:
        self.ui.e118.setChecked(v == 1)

    @property
    def e119(self) -> int:
        return 1 if self.ui.e124.currentText() == 'Kin' else 0

    @e119.setter
    def e119(self, v: int) -> None:
        pass

    @property
    def e120(self) -> int | None:
        idx = self._get_combobox_selection(self.ui.e120)
        return idx if idx is not None and idx > 0 else None

    @e120.setter
    def e120(self, v: int) -> None:
        if v is not None and v != 0:
            self._set_combobox_selection(self.ui.e120, v)

    @property
    def e121(self) -> int:
        return self._get_combobox_selection(self.ui.e121, 1)

    @e121.setter
    def e121(self, v: int) -> None:
        self._set_combobox_selection(self.ui.e121, v, -1)
        self._e121_changed()

    @property
    def e122(self) -> int:
        return self._get_int_field(self.ui.e122)

    @e122.setter
    def e122(self, v: int) -> None:
        self._set_int_field(self.ui.e122, v)

    @property
    def e123(self) -> int:
        return self._get_combobox_selection(self.ui.e123, 1)

    @e123.setter
    def e123(self, v: int) -> None:
        self._set_combobox_selection(self.ui.e123, v, -1)
        self._e123_changed()

    @property
    def e124(self) -> int:
        return self._get_combobox_selection(self.ui.e124, 1)

    @e124.setter
    def e124(self, v: int) -> None:
        self._set_combobox_selection(self.ui.e124, v, -1)

    @property
    def e125(self) -> int:
        return self._get_int_field(self.ui.e125)

    @e125.setter
    def e125(self, v: int) -> None:
        self._set_int_field(self.ui.e125, v)

    @property
    def e126(self) -> int:
        return self._get_radio_button(self.ui.e126)

    @e126.setter
    def e126(self, v: int) -> None:
        self._set_radio_button(self.ui.e126, v)

    @property
    def e127(self) -> int:
        return 1 if self.ui.e127.isChecked() else 0

    @e127.setter
    def e127(self, v: int) -> None:
        self.ui.e127.setChecked(v == 1)

    @property
    def e128(self) -> int:
        return 1 if self.ui.e128.isChecked() else 0

    @e128.setter
    def e128(self, v: int) -> None:
        self.ui.e128.setChecked(v == 1)

    @property
    def e129(self) -> int:
        return 1 if self.ui.e129.isChecked() else 0

    @e129.setter
    def e129(self, v: int) -> None:
        self.ui.e129.setChecked(v == 1)

    @property
    def e130(self) -> int:
        return 1 if self.ui.e130.isChecked() else 0

    @e130.setter
    def e130(self, v: int) -> None:
        self.ui.e130.setChecked(v == 1)

    @property
    def e131(self) -> int:
        return 1 if self.ui.e131.isChecked() else 0

    @e131.setter
    def e131(self, v: int) -> None:
        self.ui.e131.setChecked(v == 1)

    @property
    def e132(self) -> int:
        return 1 if self.ui.e132.isChecked() else 0

    @e132.setter
    def e132(self, v: int) -> None:
        self.ui.e132.setChecked(v == 1)

    @property
    def e133(self) -> int:
        return 1 if self.ui.e133.isChecked() else 0

    @e133.setter
    def e133(self, v: int) -> None:
        self.ui.e133.setChecked(v == 1)

    @property
    def e134(self) -> int:
        return self._get_radio_button(self.ui.e134)

    @e134.setter
    def e134(self, v: int) -> None:
        self._set_radio_button(self.ui.e134, v)

    @property
    def e135(self) -> int:
        return self._get_radio_button(self.ui.e135)

    @e135.setter
    def e135(self, v: int) -> None:
        self._set_radio_button(self.ui.e135, v)

    @property
    def e136(self) -> int:
        return self._get_int_field(self.ui.e136)

    @e136.setter
    def e136(self, v: int) -> None:
        self._set_int_field(self.ui.e136, v)

    @property
    def e137(self) -> int:
        return self._get_radio_button(self.ui.e137)

    @e137.setter
    def e137(self, v: int) -> None:
        self._set_radio_button(self.ui.e137, v)

    @property
    def e138(self) -> int:
        return 1 if self.ui.e138.isChecked() else 0

    @e138.setter
    def e138(self, v: int) -> None:
        self.ui.e138.setChecked(v == 1)

    @property
    def e139(self) -> int:
        return 1 if self.ui.e139.isChecked() else 0

    @e139.setter
    def e139(self, v: int) -> None:
        self.ui.e139.setChecked(v == 1)

    @property
    def e140(self) -> int:
        return 1 if self.ui.e140.isChecked() else 0

    @e140.setter
    def e140(self, v: int) -> None:
        self.ui.e140.setChecked(v == 1)

    @property
    def e141(self) -> int:
        return 1 if self.ui.e141.isChecked() else 0

    @e141.setter
    def e141(self, v: int) -> None:
        self.ui.e141.setChecked(v == 1)

    @property
    def e142(self) -> int:
        return 1 if self.ui.e142.isChecked() else 0

    @e142.setter
    def e142(self, v: int) -> None:
        self.ui.e142.setChecked(v == 1)

    @property
    def e143(self) -> int:
        return 1 if self.ui.e143.isChecked() else 0

    @e143.setter
    def e143(self, v: int) -> None:
        self.ui.e143.setChecked(v == 1)

    @property
    def e144(self) -> int:
        return 1 if self.ui.e144.isChecked() else 0

    @e144.setter
    def e144(self, v: int) -> None:
        self.ui.e144.setChecked(v == 1)

    @property
    def e145(self) -> int:
        return self._get_radio_button(self.ui.e145)

    @e145.setter
    def e145(self, v: int) -> None:
        self._set_radio_button(self.ui.e145, v)

    @property
    def e146(self) -> int:
        return self._get_radio_button(self.ui.e146)

    @e146.setter
    def e146(self, v: int) -> None:
        self._set_radio_button(self.ui.e146, v)
