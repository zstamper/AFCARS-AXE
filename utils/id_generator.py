from random import choices

_population = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/"


def generate_id() -> str:
    return "".join(choices(_population, k=12))
