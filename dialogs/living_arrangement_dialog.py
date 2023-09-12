from PySide6.QtWidgets import QWidget

from dialogs import BaseDialog
from model import LivingArrangement


class LivingArrangementDialog(BaseDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui: QWidget = self.load_ui('ui_living_arrangement.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        self.obj: LivingArrangement | None = None

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

        # field interactions
        ...

    def populate(self, obj: LivingArrangement):
        self.obj = obj
        self._from_obj()
        self.errors = []
        self.is_dirty = False

    def validate(self):
        self._validate()
        return len(self.errors) == 0

    def _validate(self) -> None:
        pass

    def _to_obj(self):
        ui = self.ui
        obj = self.obj

        obj.e40 = self._get_radio_button(ui.e40)
        obj.e58 = self._to_int(ui.e58.text())
        obj.e112 = self._to_int(ui.e112.text())
        obj.e113 = ui.e120.currentIndex == 0
        obj.e114 = 1 if ui.e114.isChecked() else 0
        obj.e115 = 1 if ui.e115.isChecked() else 0
        obj.e116 = 1 if ui.e116.isChecked() else 0
        obj.e117 = 1 if ui.e124.currentText() == 'Relative' else 0
        obj.e118 = 1 if ui.e118.isChecked() else 0
        obj.e119 = 1 if ui.e124.currentText() == 'Kin' else 0
        obj.e120 = ui.e120.currentIndex if ui.e120.currentIndex > 0 else None
        obj.e121 = self._get_combobox_selection(ui.e121, 1)
        obj.e122 = self._to_int(ui.e122.text())
        obj.e123 = self._get_combobox_selection(ui.e123, 1)
        obj.e124 = self._get_combobox_selection(ui.e124, 1)
        obj.e125 = self._to_int(ui.e125.text())
        obj.e126 = self._get_radio_button(ui.e126)
        obj.e127 = 1 if ui.e127.isChecked() else 0
        obj.e128 = 1 if ui.e128.isChecked() else 0
        obj.e129 = 1 if ui.e129.isChecked() else 0
        obj.e130 = 1 if ui.e130.isChecked() else 0
        obj.e131 = 1 if ui.e131.isChecked() else 0
        obj.e132 = 1 if ui.e132.isChecked() else 0
        obj.e133 = 1 if ui.e133.isChecked() else 0
        obj.e134 = self._get_radio_button(ui.e134)
        obj.e135 = self._get_radio_button(ui.e135)
        obj.e136 = self._to_int(ui.e136.text())
        obj.e137 = self._get_radio_button(ui.e137)
        obj.e138 = 1 if ui.e138.isChecked() else 0
        obj.e139 = 1 if ui.e139.isChecked() else 0
        obj.e140 = 1 if ui.e140.isChecked() else 0
        obj.e141 = 1 if ui.e141.isChecked() else 0
        obj.e142 = 1 if ui.e142.isChecked() else 0
        obj.e143 = 1 if ui.e143.isChecked() else 0
        obj.e144 = 1 if ui.e144.isChecked() else 0
        obj.e145 = self._get_radio_button(ui.e145)
        obj.e146 = self._get_radio_button(ui.e146)

    def _from_obj(self):
        ui = self.ui
        obj = self.obj

        self._set_radio_button(ui.e40, obj.e40)
        self._set_int_field(ui.e58, obj.e58)
        self._set_int_field(ui.e112, obj.e112)
        ui.e114.setChecked(obj.e114 == 1)
        ui.e115.setChecked(obj.e115 == 1)
        ui.e116.setChecked(obj.e116 == 1)
        # ui.e117.setChecked(obj.e117 == 1)
        ui.e118.setChecked(obj.e118 == 1)
        # ui.e119.setChecked(obj.e119 == 1)
        ui.e120.setCurrentIndex(0 if obj.e113 == 1 else obj.e120 if obj.e120 is not None else -1)
        self._set_combobox_selection(ui.e121, obj.e121, -1)
        self._set_int_field(ui.e122, obj.e122)
        self._set_combobox_selection(ui.e123, obj.e123, -1)
        self._set_combobox_selection(ui.e124, obj.e124, -1)
        self._set_int_field(ui.e125, obj.e125)
        self._set_radio_button(ui.e126, obj.e126)
        ui.e127.setChecked(obj.e127 == 1)
        ui.e128.setChecked(obj.e128 == 1)
        ui.e129.setChecked(obj.e129 == 1)
        ui.e130.setChecked(obj.e130 == 1)
        ui.e131.setChecked(obj.e131 == 1)
        ui.e132.setChecked(obj.e132 == 1)
        ui.e133.setChecked(obj.e133 == 1)
        self._set_radio_button(ui.e134, obj.e134)
        self._set_radio_button(ui.e135, obj.e135)
        self._set_int_field(ui.e136, obj.e136)
        self._set_radio_button(ui.e137, obj.e137)
        ui.e138.setChecked(obj.e138 == 1)
        ui.e139.setChecked(obj.e139 == 1)
        ui.e140.setChecked(obj.e140 == 1)
        ui.e141.setChecked(obj.e141 == 1)
        ui.e142.setChecked(obj.e142 == 1)
        ui.e143.setChecked(obj.e143 == 1)
        ui.e144.setChecked(obj.e144 == 1)
        self._set_radio_button(ui.e145, obj.e145)
        self._set_radio_button(ui.e146, obj.e146)
