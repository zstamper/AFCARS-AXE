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

def afcars_to_date(d: int) -> date:
    year = d // 10000
    month = (d - (d // 10000) * 10000) // 100
    day = d - (d // 100) * 100
    return date(year=year, month=month, day=day)
