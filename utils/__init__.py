from .id_generator import generate_id


def coalesce(v: str|int|float|None, d: int|float) -> int|float:
    if isinstance(v,(int,float)):
        return v
    if isinstance(v, str):
        try:
            return int(v)
        except ValueError:
            try:
                return float(v)
            except ValueError:
                return d
    return d