import controllers.a_controller
import controllers.ooh_controller
import model
from controllers.child_controller import ChildController
from model.models import ReportType


class TestChildController:

    def test_do_add_ooh(self, qtbot, mocker):
        mocker.patch('dialogs.child_dialog.ChildDialog', window_title="test", agency_name="test agency",
                     agency_code="1", reporting_period="202303", report_type=ReportType.OOH)
        mocker.patch('controllers.ooh_controller.OOHController.add')
        mocker.patch('controllers.a_controller.AController.add')
        mocker.patch('model.ChildTable.persist_model')
        mocker.patch('controllers.child_controller.ChildController.fetch_child_data')
        controller = ChildController()
        controller.report_type = ReportType.OOH
        controller.do_add()
        controllers.ooh_controller.OOHController.add.assert_called_once()
        controllers.a_controller.AController.add.assert_not_called()
        model.ChildTable.persist_model.assert_called_once()

    def test_do_add_a(self, qtbot, mocker):
        mocker.patch('dialogs.child_dialog.ChildDialog', window_title="test", agency_name="test agency",
                     agency_code="1", reporting_period="202303", report_type=ReportType.A)
        mocker.patch('controllers.ooh_controller.OOHController.add')
        mocker.patch('controllers.a_controller.AController.add')
        mocker.patch('model.ChildTable.persist_model')
        mocker.patch('controllers.child_controller.ChildController.fetch_child_data')

        controller = ChildController()
        controller.report_type = ReportType.A
        controller.do_add()
        controllers.ooh_controller.OOHController.add.assert_not_called()
        controllers.a_controller.AController.add.assert_called_once()
        model.ChildTable.persist_model.assert_called_once()

    def test_do_edit_ooh(self, qtbot, mocker):
        mocker.patch('dialogs.child_dialog.ChildDialog', window_title="test", agency_name="test agency",
                     agency_code="1", reporting_period="202303", report_type=ReportType.OOH)
        mocker.patch('controllers.ooh_controller.OOHController.edit')
        mocker.patch('controllers.a_controller.AController.edit')
        mocker.patch('model.ChildTable.persist_model')
        mocker.patch('controllers.child_controller.ChildController.fetch_child_data')
        controller = ChildController()
        controller.report_type = ReportType.OOH
        controller.do_edit()
        controllers.ooh_controller.OOHController.edit.assert_called_once()
        controllers.a_controller.AController.edit.assert_not_called()
        model.ChildTable.persist_model.assert_called_once()

    def test_do_edit_a(self, qtbot, mocker):
        mocker.patch('dialogs.child_dialog.ChildDialog', window_title="test", agency_name="test agency",
                     agency_code="1", reporting_period="202303", report_type=ReportType.A)
        mocker.patch('controllers.ooh_controller.OOHController.edit')
        mocker.patch('controllers.a_controller.AController.edit')
        mocker.patch('model.ChildTable.persist_model')
        mocker.patch('controllers.child_controller.ChildController.fetch_child_data')
        controller = ChildController()
        controller.report_type = ReportType.A
        controller.do_edit()
        controllers.ooh_controller.OOHController.edit.assert_not_called()
        controllers.a_controller.AController.edit.assert_called_once()
        model.ChildTable.persist_model.assert_called_once()
