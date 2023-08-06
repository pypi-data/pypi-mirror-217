from dataclasses import dataclass

from atoti_core import Identifier

from .._external_table_identifier import ExternalTableIdentifier


@dataclass(frozen=True)
class ExternalColumnIdentifier(Identifier):  # pylint: disable=keyword-only-dataclass
    table_identifier: ExternalTableIdentifier
    column_name: str

    @property
    def key(self) -> tuple[str, str]:
        return self.table_identifier.table_name, self.column_name

    def __repr__(self) -> str:
        return f"""{self.table_identifier!r}["{self.column_name}"]"""
