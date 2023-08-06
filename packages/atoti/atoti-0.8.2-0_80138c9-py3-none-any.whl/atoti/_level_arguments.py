from atoti_core import ColumnIdentifier

from .order._order import Order
from .type import DataType

LevelArguments = tuple[str, ColumnIdentifier, DataType, Order]
