import os
import sys
import pytest
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt
from dialogs.childform import ChildForm

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def child_form(qtbot):
    form = ChildForm()
    qtbot.addWidget(form)
    yield form
    del form


def test_cannot_have_abandoned_with_any_other_race(child_form, qtbot):
    child_form.ui.e19.click()

    assert not child_form.ui.e13.isEnabled()
    assert not child_form.ui.e14.isEnabled()
    assert not child_form.ui.e15.isEnabled()
    assert not child_form.ui.e16.isEnabled()
    assert not child_form.ui.e17.isEnabled()
    assert not child_form.ui.e18.isEnabled()
    assert not child_form.ui.e20.isEnabled()


def test_cannot_have_declined_with_any_other_race(child_form, qtbot):
    child_form.ui.e20.click()

    assert not child_form.ui.e13.isEnabled()
    assert not child_form.ui.e14.isEnabled()
    assert not child_form.ui.e15.isEnabled()
    assert not child_form.ui.e16.isEnabled()
    assert not child_form.ui.e17.isEnabled()
    assert not child_form.ui.e18.isEnabled()
    assert not child_form.ui.e19.isEnabled()


def test_adoption_in_another_country_is_required_when_prior_adoption_date_is_entered(child_form, qtbot):
    child_form.ui.e19.setChecked(False)
    child_form.ui.e42.setText('')
    assert child_form.ui.e43_error.text().find(child_form.E43_ERROR_MESSAGE) == -1

    child_form.ui.e42.setText('202001')
    assert child_form.ui.e43_error.text().find(child_form.E43_ERROR_MESSAGE) >= 0


def test_cannot_enter_in_more_siblings_in_foster_care_than_total_siblings(child_form, qtbot):
    child_form.ui.e56.setText('1')
    child_form.ui.e57.setText('1')
    assert child_form.ui.e57_error.text() == ""

    child_form.ui.e57.setText('2')
    assert child_form.ui.e57_error.text().find(child_form.E57_ERROR_MESSAGE) >= 0


def test_cannot_have_siblings_in_placement_if_E57_is_0(child_form, qtbot):
    # E58
    assert False


def test_generate_id(child_form, qtbot):
    child_form.ui.e4_generate.click()
    assert child_form.ui.e4.text() != ""
    assert not child_form.ui.e4.isEnabled()
    assert not child_form.ui.e4_generate.isEnabled()


def test_id_field_is_disabled_when_valid_id_is_entered(child_form, qtbot):
    child_form.ui.e4.setText('0')
    assert child_form.ui.e4.isEnabled()
    assert child_form.ui.e4_generate.isEnabled()
    child_form.ui.e4.setText('00')
    assert child_form.ui.e4.isEnabled()
    assert child_form.ui.e4_generate.isEnabled()
    child_form.ui.e4.setText('000')
    assert child_form.ui.e4.isEnabled()
    assert child_form.ui.e4_generate.isEnabled()
    child_form.ui.e4.setText('0000')
    assert child_form.ui.e4.isEnabled()
    assert child_form.ui.e4_generate.isEnabled()
    child_form.ui.e4.setText('00000')
    assert child_form.ui.e4.isEnabled()
    assert child_form.ui.e4_generate.isEnabled()
    child_form.ui.e4.setText('000000')
    assert child_form.ui.e4.isEnabled()
    assert child_form.ui.e4_generate.isEnabled()
    child_form.ui.e4.setText('0000000')
    assert child_form.ui.e4.isEnabled()
    assert child_form.ui.e4_generate.isEnabled()
    child_form.ui.e4.setText('00000000')
    assert child_form.ui.e4.isEnabled()
    assert child_form.ui.e4_generate.isEnabled()
    child_form.ui.e4.setText('000000000')
    assert child_form.ui.e4.isEnabled()
    assert child_form.ui.e4_generate.isEnabled()
    child_form.ui.e4.setText('0000000000')
    assert child_form.ui.e4.isEnabled()
    assert child_form.ui.e4_generate.isEnabled()
    child_form.ui.e4.setText('00000000000')
    assert child_form.ui.e4.isEnabled()
    assert child_form.ui.e4_generate.isEnabled()
    child_form.ui.e4.setText('000000000000')
    assert not child_form.ui.e4.isEnabled()
    assert not child_form.ui.e4_generate.isEnabled()


def test_if_e42_is_empty_e41_is_no(child_form, qtbot):
    child_form.ui.e42.setText('')
    assert child_form.e41 == 0


def test_if_e42_is_filled_e41_is_yes(child_form, qtbot):
    child_form.ui.e42.setText('202001')
    assert child_form.e41 == 1


def test_if_e19_is_checked_e41_is_abandonded(child_form, qtbot):
    child_form.ui.e19.click()
    assert child_form.e41 == 7


def test_if_e45_is_empty_e44_is_no(child_form, qtbot):
    child_form.ui.e45.setText('')
    assert child_form.e44 == 0


def test_if_e45_is_filled_e44_is_yes(child_form, qtbot):
    child_form.ui.e45.setText('202001')
    assert child_form.e44 == 1


def test_if_e19_is_checked_e44_is_abandoned(child_form, qtbot):
    # hmm... there is no specific e44 data element. This appears to be a virtual element instead.
    child_form.ui.e19.click()
    assert child_form.e44 == 7


def test_if_child_has_diagnosed_condition_one_of_e24_to_e34_must_be_selected(child_form, qtbot):
    child_form.ui.e23.setCurrentIndex(1)
    child_form.ui.e24.setCurrentIndex(-1)
    child_form.ui.e25.setCurrentIndex(-1)
    child_form.ui.e26.setCurrentIndex(-1)
    child_form.ui.e27.setCurrentIndex(-1)
    child_form.ui.e28.setCurrentIndex(-1)
    child_form.ui.e29.setCurrentIndex(-1)
    child_form.ui.e30.setCurrentIndex(-1)
    child_form.ui.e31.setCurrentIndex(-1)
    child_form.ui.e32.setCurrentIndex(-1)
    child_form.ui.e33.setCurrentIndex(-1)
    child_form.ui.e34.setCurrentIndex(-1)
    assert child_form.ui.e24_error.text().find(child_form.E24_ERROR_MESSAGE) >= 0


def test_if_child_does_not_have_diagnosed_condition_none_of_e24_to_e34_are_enabled(child_form, qtbot):
    # index 0 == "No exam or assessment conducted (unknown)"
    child_form.ui.e23.setCurrentIndex(0)
    assert not child_form.ui.e24.isEnabled()
    assert not child_form.ui.e25.isEnabled()
    assert not child_form.ui.e26.isEnabled()
    assert not child_form.ui.e27.isEnabled()
    assert not child_form.ui.e28.isEnabled()
    assert not child_form.ui.e29.isEnabled()
    assert not child_form.ui.e30.isEnabled()
    assert not child_form.ui.e31.isEnabled()
    assert not child_form.ui.e32.isEnabled()
    assert not child_form.ui.e33.isEnabled()
    assert not child_form.ui.e34.isEnabled()

    # index 1 == "Child has a diagnosed condition"
    child_form.ui.e23.setCurrentIndex(1)
    assert child_form.ui.e24.isEnabled()
    assert child_form.ui.e25.isEnabled()
    assert child_form.ui.e26.isEnabled()
    assert child_form.ui.e27.isEnabled()
    assert child_form.ui.e28.isEnabled()
    assert child_form.ui.e29.isEnabled()
    assert child_form.ui.e30.isEnabled()
    assert child_form.ui.e31.isEnabled()
    assert child_form.ui.e32.isEnabled()
    assert child_form.ui.e33.isEnabled()
    assert child_form.ui.e34.isEnabled()

    # index 2 == "Exam or assessment conducted and child none of the conditions apply"
    child_form.ui.e23.setCurrentIndex(2)
    assert not child_form.ui.e24.isEnabled()
    assert not child_form.ui.e25.isEnabled()
    assert not child_form.ui.e26.isEnabled()
    assert not child_form.ui.e27.isEnabled()
    assert not child_form.ui.e28.isEnabled()
    assert not child_form.ui.e29.isEnabled()
    assert not child_form.ui.e30.isEnabled()
    assert not child_form.ui.e31.isEnabled()
    assert not child_form.ui.e32.isEnabled()
    assert not child_form.ui.e33.isEnabled()
    assert not child_form.ui.e34.isEnabled()

    # index 3 == "Exam or assessment conducted but results not received (unknown)"
    child_form.ui.e23.setCurrentIndex(3)
    assert not child_form.ui.e24.isEnabled()
    assert not child_form.ui.e25.isEnabled()
    assert not child_form.ui.e26.isEnabled()
    assert not child_form.ui.e27.isEnabled()
    assert not child_form.ui.e28.isEnabled()
    assert not child_form.ui.e29.isEnabled()
    assert not child_form.ui.e30.isEnabled()
    assert not child_form.ui.e31.isEnabled()
    assert not child_form.ui.e32.isEnabled()
    assert not child_form.ui.e33.isEnabled()
    assert not child_form.ui.e34.isEnabled()


def test_if_child_is_male_child_cannot_be_pregnant(child_form, qtbot):
    # if e6 is Female, e38 is enabled
    child_form.ui.e6_f.click()
    assert child_form.ui.e38.isEnabled()

    # if e6 is Male, e38 is disabled
    child_form.ui.e6_m.click()
    assert not child_form.ui.e38.isEnabled()


def test_icwa_funding_button(child_form, qtbot):
    child_form.ui.funding_yes.click()
    assert not child_form.ui.e7_y.isEnabled()
    assert not child_form.ui.e7_n.isEnabled()
    assert child_form.ui.e7_required.isHidden()
    assert not child_form.ui.e8_y.isEnabled()
    assert not child_form.ui.e8_n.isEnabled()
    assert not child_form.ui.e8_u.isEnabled()
    assert child_form.ui.e8_required.isHidden()
    assert not child_form.ui.e9.isEnabled()
    assert child_form.ui_e9.isHidden()
    assert not child_form.ui.e10_y.isEnabled()
    assert not child_form.ui.e10_n.isEnabled()
    assert not child_form.ui.e10_u.isEnabled()
    assert child_form.ui.e10_required.isHidden()
    assert not child_form.ui.e11.isEnabled()
    assert child_form.ui.e11_required.isHidden()
    assert not child_form.ui.e12_y.isEnabled()
    assert not child_form.ui.e12_n.isEnabled()
    assert child_form.ui.e12_required.isHidden()

    # TODO: If Yes is indicated, Element 104 is populated with “applies”

    child_form.ui.funding_no.click()
    assert child_form.ui.e7_y.isEnabled()
    assert child_form.ui.e7_n.isEnabled()
    assert not child_form.ui.e7_required.isHidden()
    assert child_form.ui.e8_y.isEnabled()
    assert child_form.ui.e8_n.isEnabled()
    assert child_form.ui.e8_u.isEnabled()
    assert not child_form.ui.e8_required.isHidden()
    assert child_form.ui.e9.isEnabled()
    assert not child_form.ui.e9_required.isHidden()
    assert child_form.ui.e10_y.isEnabled()
    assert child_form.ui.e10_n.isEnabled()
    assert child_form.ui.e10_u.isEnabled()
    assert not child_form.ui.e10_required.isHidden()
    assert child_form.ui.e11.isEnabled()
    assert not child_form.ui.e11_required.isHidden()
    assert child_form.ui.e12_y.isEnabled()
    assert child_form.ui.e12_n.isEnabled()
    assert not child_form.ui.e12_required.isHidden()
    # TODO: If No is indicated, Element 104 is populated with “applies”

    assert False


def test_e9_is_required_when_e8_is_yes(child_form, qtbot):
    child_form.ui.e8_y.click()
    assert not child_form.ui.e9_required.isHidden()

    child_form.ui.e8_n.click()
    assert child_form.ui.e9_required.isHidden()

    child_form.ui.e8_u.click()
    assert child_form.ui.e9_required.isHidden()

    child_form.ui.e8_y.click()
    child_form.ui.e9.setSelectedIndexes([0])
    assert child_form.ui.e9_required.isHidden()

    child_form.ui.e8_y.click()
    child_form.ui.e9.setSelectedIndexes([])
    assert not child_form.ui.e9_required.isHidden()


def test_e11_is_required_when_e10_is_yes(child_form, qtbot, today):
    child_form.ui.e10_y.click()
    assert not child_form.ui.e11_required.isHidden()

    child_form.ui.e10_n.click()
    assert child_form.ui.e11_required.isHidden()

    child_form.ui.e10_u.click()
    assert child_form.ui.e11_required.isHidden()

    child_form.ui.e10_y.click()
    child_form.ui.e11.setText(today.strftime('%Y%m%d'))
    assert child_form.ui.e11_required.isHidden()

    child_form.ui.e10_y.click()
    child_form.ui.e11.setText(None)
    assert not child_form.ui.e11_required.isHidden()


def test_e12_is_required_when_e10_is_yes(child_form, qtbot):
    # given E12 is not clicked at all
    child_form.ui.e10_y.click()
    assert not child_form.ui.e12_required.isHidden()

    child_form.ui.e10_n.click()
    assert child_form.ui.e12_required.isHidden()

    child_form.ui.e10_u.click()
    assert child_form.ui.e12_required.isHidden()

    child_form.ui.e12_y.click()
    child_form.ui.e10_y.click()
    assert child_form.ui.e12_required.isHidden()

    child_form.ui.e10_n.click()
    assert child_form.ui.e12_required.isHidden()

    child_form.ui.e10_u.click()
    assert child_form.ui.e12_required.isHidden()

    child_form.ui.e12_n.click()
    child_form.ui.e10_y.click()
    assert child_form.ui.e12_required.isHidden()

    child_form.ui.e10_n.click()
    assert child_form.ui.e12_required.isHidden()

    child_form.ui.e10_u.click()
    assert child_form.ui.e12_required.isHidden()


def test_e43_is_required_if_e42_is_not_empty(child_form, qtbot):
    assert False


def test_e57_cannot_be_bigger_than_e56(child_form, qtbot):
    assert False


