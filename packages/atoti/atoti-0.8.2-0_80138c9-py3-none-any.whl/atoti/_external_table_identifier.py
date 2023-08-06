from dataclasses import dataclass

from atoti_core import Identifier


@dataclass(frozen=True)
class ExternalTableIdentifier(Identifier):  # pylint: disable=keyword-only-dataclass
    database_name: str
    schema_name: str
    table_name: str

    @property
    def key(self) -> tuple[str, str, str]:
        return self.database_name, self.schema_name, self.table_name

    def __repr__(self) -> str:
        return f"""t[{self.key}]"""
