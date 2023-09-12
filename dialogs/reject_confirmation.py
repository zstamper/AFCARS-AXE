from PySide6.QtWidgets import QMessageBox


def reject_confiration() -> int:
    msg_box = QMessageBox()
    msg_box.setText("The record has been modified.")
    msg_box.setInformativeText("Do you want to save your changed?")
    msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
    msg_box.setDefaultButton(QMessageBox.Save)
    return msg_box.exec()