from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING, Any, Dict

from .Signal import Signals

if TYPE_CHECKING:
    from .DoubleNetwork import DoubleNetwork


nodes: Dict[int, ASTNode] = {}


class ASTNode(ABC):
    def __init__(
        self,
        name: str,
        output_network: Optional[DoubleNetwork] = None,
        nid: Optional[int] = None,
    ):
        self.name: str = name
        self.output_network: Optional[DoubleNetwork] = output_network
        self.previous_result: Optional[Signals] = None
        self.id = nid if nid is not None else max([*nodes.keys(), 0]) + 1
        nodes[self.id] = self

    @abstractmethod
    def tick(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def cli_repr(self) -> str:
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ASTNode):
            return (
                self.name == other.name and self.output_network == other.output_network
            )
        return False  # pragma: no cover
