from typing import Optional

_e1: Optional[str] = None


def E1() -> str:
    global _e1
    return _e1


def set_E1(v: str) -> None:
    global _e1
    _e1 = v


def is_state() -> bool:
    return False if E1() is None else len(E1()) == 2


def is_tribe() -> bool:
    return False if E1() is None else len(E1()) == 3
