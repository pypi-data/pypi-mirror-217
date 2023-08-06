from dataclasses import dataclass
from itertools import chain
from typing import Optional

from atoti_core import (
    Identifier,
    IdentifierT,
    Operand,
    Operation,
    keyword_only_dataclass,
)


@keyword_only_dataclass
@dataclass(eq=False, frozen=True)
class FunctionOperation(Operation[IdentifierT]):
    function_key: str
    operands: tuple[Optional[Operand[IdentifierT]], ...] = ()

    @property
    def _identifier_types(self) -> frozenset[type[Identifier]]:
        return frozenset(
            chain(*(self._get_identifier_types(operand) for operand in self.operands))
        )
