import datetime

import pytest


@pytest.fixture
def today():
    return datetime.date.today()