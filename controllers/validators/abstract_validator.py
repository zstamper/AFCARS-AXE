from abc import ABC, abstractmethod


class AbstractValidator(ABC):
    # TODO: refactor this whole mess to use generics or the Python equivalent

    @abstractmethod
    def __init__(self, dialog):
        ...

    @abstractmethod
    def validate_tab(self, tab: int) -> bool:
        ...

    @abstractmethod
    def validate(self) -> bool:
        ...

    @abstractmethod
    def messages(self) -> list:
        ...
