from PySide6.QtWidgets import QWidget

from dialogs import BaseDialog


class PermanencyHearingDialog(BaseDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui: QWidget = self.load_ui('ui_permanency_hearing.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())

    def _wire_ui(self):
        self.setModal(True)
        self.ui.form_action.accepted.connect(self.accept)
        self.ui.form_action.rejected.connect(self.reject)

    @property
    def e150(self) -> int | None:
        return self._get_int_field(self.ui.e150)

    @e150.setter
    def e150(self, v: int) -> None:
        self._set_int_field(self.ui.e150, v)
