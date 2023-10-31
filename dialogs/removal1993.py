from typing import Callable, Optional, Any

from PySide6.QtWidgets import QWidget

from . import BaseDialog


class Removal1993Dialog(BaseDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui: QWidget = self.load_ui('ui_removal1993.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        self.id: int | None = None
        self.ooh_id: int | None = None
        self._child_name: str = ""
        # self.on_accept: Optional[Callable] = None

    # def accept(self):
    #     if self.on_accept and self.on_accept():
    #         super().accept()

    # ------------------------------------------------------------------------

    def clear(self) -> None:
        super().clear()
        self.child_name = ""
        self.id = None
        self.ooh = None

    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self, id: int | None) -> None:
        self.__id = id

    @property
    def ooh(self) -> Any:
        return self.__ooh

    @ooh.setter
    def ooh(self, ooh: Any) -> None:
        self.__ooh = ooh

    @property
    def child_name(self) -> str:
        return self._child_name

    @child_name.setter
    def child_name(self, v: str):
        self._child_name = v
        if v:
            self.setWindowTitle(f"1993 Removal : {v}")
        else:
            self.setWindowTitle("")

    @property
    def e69(self) -> int | None:
        return self._get_int_field(self.ui.e69)

    @e69.setter
    def e69(self, v: int) -> None:
        self._set_int_field(self.ui.e69, v)

    @property
    def e153(self) -> int | None:
        return self._get_int_field(self.ui.e153)

    @e153.setter
    def e153(self, v: int):
        self._set_int_field(self.ui.e153, v)

    @property
    def e155(self) -> int | None:
        return self._get_combobox_selection(self.ui.e155, mapping={0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 8})

    @e155.setter
    def e155(self, v: int):
        self._set_combobox_selection(self.ui.e155, v, mapping={1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 8: 6})

    # ------------------------------------------------------------------------

    def _wire_ui(self):
        self.setModal(True)

        ui = self.ui
        """add event handlers to the form"""
        ui.form_action.accepted.connect(self.accept)
        ui.form_action.rejected.connect(self.reject)
