from collections.abc import Iterable
from typing import Protocol

from atoti_core import DataType, IdentifierT


class GetDataTypes(Protocol):
    def __call__(
        self, identifier: Iterable[IdentifierT], /, *, cube_name: str
    ) -> dict[IdentifierT, DataType]:
        ...
