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
