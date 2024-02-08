from typing import Optional, Callable

from PySide6.QtWidgets import QWidget

from dialogs import BaseDialog


class PermanencyPlanDialog(BaseDialog):
    obj_to_e148_mapping = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4}
    e148_to_obj_mapping = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui: QWidget = self.load_ui('ui_permanency_plan.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        self.id: int | None = None
        self.removal_id: int | None = None
        self._child_name: str = ""
        self.on_validate: Optional[Callable] = None
        self.on_save: Optional[Callable] = None
        self.on_close: Optional[Callable] = None

    def _wire_ui(self) -> None:
        self.setModal(True)

        self.ui.validate_button.clicked.connect(self.validate_button_clicked)
        self.ui.save_button.clicked.connect(self.save_button_clicked)
        self.ui.close_button.clicked.connect(self.close_button_clicked)

    def validate_button_clicked(self):
        if self.on_validate:
            self.on_validate()

    def save_button_clicked(self):
        if self.on_save:
            self.on_save()

    def close_button_clicked(self):
        if not self.on_close or self.on_close():
            self.close()

    def clear(self, exclude: list[str] = None) -> None:
        super().clear()
        self.child_name = ""

    @property
    def child_name(self) -> str:
        return self._child_name

    @child_name.setter
    def child_name(self, v: str) -> None:
        self._child_name = v
        if v:
            self.setWindowTitle(f"Permanency Plan : {v}")
        else:
            self.setWindowTitle("")

    @property
    def e147(self) -> int | None:
        return self._get_int_field(self.ui.e147)

    @e147.setter
    def e147(self, v: int) -> None:
        self._set_int_field(self.ui.e147, v)

    @property
    def e148(self) -> int | None:
        return self._get_combobox_selection(self.ui.e148, self.e148_to_obj_mapping)

    @e148.setter
    def e148(self, v: int) -> None:
        self._set_combobox_selection(self.ui.e148, v, self.obj_to_e148_mapping)
