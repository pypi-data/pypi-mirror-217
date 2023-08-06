from dataclasses import dataclass
from itertools import chain
from typing import Optional

from atoti_core import (
    Identifier,
    IdentifierT,
    Operand,
    OperandCondition,
    Operation,
    keyword_only_dataclass,
)


@keyword_only_dataclass
@dataclass(eq=False, frozen=True)
class WhereOperation(Operation[IdentifierT]):
    condition: OperandCondition[IdentifierT]
    true_value: Operand[IdentifierT]
    false_value: Optional[Operand[IdentifierT]]

    @property
    def _identifier_types(self) -> frozenset[type[Identifier]]:
        operands = [
            self.condition,
            self.true_value,
            self.false_value,
        ]
        return frozenset(
            chain(
                *(
                    self._get_identifier_types(
                        operand,
                    )
                    for operand in operands
                )
            )
        )
