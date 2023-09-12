from PySide6.QtWidgets import QWidget

from model import Removal2020, Removal1993
from . import BaseDialog


class Removal1993Dialog(BaseDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui: QWidget = self.load_ui('ui_removal1993.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        self.obj: Removal2020 | None = None

    def populate(self, obj: Removal1993):
        self.obj = obj
        self._from_obj()
        self.errors = []
        self.is_dirty = False

    def validate(self):
        self._validate()
        return len(self.errors) == 0

    # ------------------------------------------------------------------------

    def _wire_ui(self):
        self.setModal(True)

        ui = self.ui
        """add event handlers to the form"""
        ui.form_action.accepted.connect(self.accept)
        ui.form_action.rejected.connect(self.reject)

    def _validate(self):
        """validates the form by iterating over the validation rules, return true if the error message list is empty"""
        ...

    def _to_obj(self):
        """copy form field contents into the model"""
        ui = self.ui
        obj = self.obj
        obj.e69 = self._get_int_field(ui.e69)
        obj.e153 = self._get_int_field(ui.e153)
        obj.e155 = self._get_combobox_selection(ui.e155, mapping={0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 8})

    def _from_obj(self):
        """copy model fields into the form"""
        ui = self.ui
        obj = self.obj

        self._set_int_field(ui.e69, obj.e69)
        self._set_int_field(ui.e153, obj.e153)
        self._set_combobox_selection(ui.e155, obj.e155, mapping={1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 8: 6})
