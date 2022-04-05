from typing import Any, Dict, Optional

from pydantic import BaseModel, Field
from PySide6.QtCore import Property, QObject


class Criterion(BaseModel):
    name: str
    type: str
    default: Optional[Any] = None
    data: Dict[str, Any] = Field(default_factory=dict)


class CriterionProxy(QObject):
    """A labeling criterion, currently supports "choice" and "bool"."""

    def __init__(self, criterion: Criterion, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._criterion = criterion

    @Property(str, constant=True)
    def name(self) -> str:
        return self._criterion.name

    @Property(str, constant=True)
    def type(self) -> str:
        return self._criterion.type

    @Property("QVariant", constant=True)
    def default(self) -> Any:
        return self._criterion.default

    @Property("QVariant", constant=True)
    def data(self) -> Dict[str, Any]:
        return self._criterion.data
