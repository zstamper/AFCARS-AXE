from PySide6.QtWidgets import QWidget

from dialogs import BaseDialog
from model import PermanencyHearing


class PermanencyHearingDialog(BaseDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui: QWidget = self.load_ui('ui_permanency_hearing.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        self.obj: PermanencyHearing | None = None

    def _wire_ui(self):
        self.setModal(True)
        self.ui.form_action.accepted.connect(self.accept)
        self.ui.form_action.rejected.connect(self.reject)

    def populate(self, obj: PermanencyHearing):
        self.obj = obj
        self._from_obj()
        self.errors = []
        self.is_dirty = False

    def _from_obj(self):
        self._set_text_field(self.ui.e150, self.obj.e150)

    def _to_obj(self):
        self.obj.e150 = self.ui.e150.text()
