# Copyright 2024 by ICF International, Inc.
#
# This file is part of AXE, the AFCARS XML Editor.
#
# AXE is free software: you can redistribute it and/or modify it under the terms
# of the GNU Lesser General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# AXE is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# AXE. If not, see <https://www.gnu.org/licenses/>.

from datetime import date
from typing import Optional

_e1: Optional[str] = None
_e2: Optional[str] = None


def E1() -> str:
    global _e1
    return _e1


def set_E1(v: str) -> None:
    global _e1
    _e1 = v


def E2() -> str:
    global _e2
    return _e2


def set_E2(v: str) -> None:
    global _e2
    _e2 = v


def e2_start_date() -> date:
    year = int(E2()[:4])
    period = E2()[4:]
    if period == 'A' or period == '03':
        month = 10
        year -= 1
    elif period == 'B' or period == '09':
        month = 4
    else:
        raise ValueError("E1 format is not recognized.")
    return date(year=year, month=month, day=1)


def e2_end_date() -> date:
    year = int(E2()[:4])
    period = E2()[4:]
    if period == 'A' or period == '03':
        month = 3
        day = 31
    elif period == 'B' or period == '09':
        month = 9
        day = 30
    else:
        raise ValueError("E1 format is not recognized.")
    return date(year=year, month=month, day=day)


def is_state() -> bool:
    return False if E1() is None else len(E1()) == 2


def is_tribe() -> bool:
    return False if E1() is None else len(E1()) == 3


def afcars_to_date(d: int) -> date | None:
    if d is None:
        return None
    year = d // 10000
    month = (d - (d // 10000) * 10000) // 100
    day = d - (d // 100) * 100
    try:
        return date(year=year, month=month, day=day)
    except ValueError:
        return None


def is_valid_date(d: int) -> bool:
    try:
        d = afcars_to_date(d)
        assert d is not None
        return True
    except ValueError:
        return False
    except AssertionError:
        return False


def is_valid_year_month(d: int) -> bool:
    if d is None:
        return False
    try:
        year = d // 100
        month = d % 100
        day = 1
        d = date(year=year, month=month, day=day)
        return True
    except (ValueError, AssertionError):
        return False


def is_future_date(d: int) -> bool:
    d = afcars_to_date(d)
    return d and d > date.today()


def is_future_year_month(d: int) -> bool:
    if d is None:
        return False
    try:
        year = d // 100
        month = d % 100
        day = 1
        d = date(year=year, month=month, day=day)
        return d > date.today()
    except (ValueError, AssertionError):
        return False


def is_way_past_date(d: int) -> bool:
    try:
        d = afcars_to_date(d)
        t = date.today()
        past = date(year=t.year - 100, month=t.month, day=t.day)
        return d and d < past
    except (ValueError, AssertionError):
        return False


def is_way_past_year_month(d: int) -> bool:
    if d is None:
        return False
    try:
        year = d // 100
        month = d % 100
        day = 1
        d = date(year=year, month=month, day=day)
        past = date(year=date.today().year - 100, month=date.today().month, day=date.today().day)
        return d < past
    except (ValueError, AssertionError):
        return False


def is_valid_adult_birth_date(d: int) -> bool:
    try:
        d = afcars_to_date(d)
        assert d is not None
        today = date.today()
        ten_years_old = date(year=today.year - 10, month=today.month, day=today.day)
        one_hundred_years_old = date(year=today.year - 100, month=today.month, day=today.day)
        return one_hundred_years_old <= d <= ten_years_old
    except (AssertionError):
        return True
