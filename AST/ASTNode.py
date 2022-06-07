from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING, Any

from .Signal import Signals

if TYPE_CHECKING:
    from .DoubleNetwork import DoubleNetwork


class ASTNode(ABC):
    def __init__(self, name: str, output_network: Optional[DoubleNetwork] = None):
        self.name: str = name
        self.output_network: Optional[DoubleNetwork] = output_network
        self.previous_result: Optional[Signals] = None

    @abstractmethod
    def tick(self) -> None:
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ASTNode):
            return (
                self.name == other.name and self.output_network == other.output_network
            )
        return False  # pragma: no cover
