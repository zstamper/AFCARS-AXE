import pytest

import model
from controllers.a_controller import AController
from controllers.ooh_controller import OOHController
from controllers.second_parent_controller import SecondParentController
from model import Child, BaseChild, OOHRecord, ARecord, SecondParent


@pytest.fixture
def database():
    model.open_database(":memory:", testing=True)
    model.create_tables()
    yield model.database
    model.close_database()


class TestSecondParentTPR:

    def test_add_parent2_is_dirty(self, qtbot, database, mocker):
        # TODO: check all the fields
        data = SecondParent(number=2)
        controller = SecondParentController(None, "", data=data)
        qtbot.addWidget(controller.dialog)

        assert not controller.is_dirty()

        controller.dialog.ui.e64_v.setChecked(True)
        assert controller.is_dirty()

    def test_add_parent2