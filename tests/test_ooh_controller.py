import pytest

import model
from controllers.a_controller import AController
from controllers.ooh_controller import OOHController
from model import Child, BaseChild, OOHRecord, ARecord


@pytest.fixture
def database():
    model.open_database(":memory:", testing=True)
    model.create_tables()
    yield model.database
    model.close_database()


class TestOOHController:

    def test_add_child(self, qtbot, database, mocker):
        child = Child()
        child.ooh = OOHRecord()
        base_child = BaseChild(last_name="TEST1")
        controller = OOHController(None, e1="000")
        controller.base_child = base_child
        controller.child = child
        qtbot.addWidget(controller.dialog.ui)
        controller.dialog.show()

        assert controller.dialog.ui.last_name.text() == 'TEST1'

        controller.dialog.ui.last_name.setText('test2')
        controller.dialog.ui.save_button.click()

        assert controller.base_child == base_child
        assert base_child.last_name == 'test2'

    def test_edit_child(self, qtbot, database, mocker):
        child = Child()
        child.ooh = OOHRecord(e10=0)
        base_child = BaseChild(last_name="TEST1")
        controller = OOHController(None, e1="000")
        controller.base_child = base_child
        controller.child = child
        qtbot.addWidget(controller.dialog.ui)
        controller.dialog.show()

        assert controller.dialog.ui.last_name.text() == 'TEST1'
        assert controller.dialog.e10 == 0

        controller.dialog.ui.last_name.setText('test2')
        controller.dialog.e10 = 1
        controller.dialog.ui.save_button.click()

        assert controller.base_child is base_child
        assert base_child.last_name == 'test2'
        assert controller.child is child
        assert controller.child.ooh is child.ooh
        assert child.ooh.e10 == 1


