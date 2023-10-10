from PySide6.QtWidgets import QWidget

from dialogs import BaseDialog


class PermanencyHearingDialog(BaseDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui: QWidget = self.load_ui('ui_permanency_hearing.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        self.id: int | None = None
        self.removal_id: int | None = None
        self._child_name: str = ""

    def _wire_ui(self):
        self.setModal(True)
        self.ui.form_action.accepted.connect(self.accept)
        self.ui.form_action.rejected.connect(self.reject)

    def clear(self):
        super().clear()
        self.child_name = ""

    @property
    def child_name(self) -> str:
        return self._child_name

    @child_name.setter
    def child_name(self, v: str):
        self._child_name = v
        if v:
            self.setWindowTitle(f"Permanency Hearing : {v}")
        else:
            self.setWindowTitle("")

    @property
    def e150(self) -> int | None:
        return self._get_int_field(self.ui.e150)

    @e150.setter
    def e150(self, v: int) -> None:
        self._set_int_field(self.ui.e150, v)
