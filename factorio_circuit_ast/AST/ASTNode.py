from __future__ import annotations

import string
from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING, Any, Dict, Tuple

from factorio_circuit_ast.Mixin import IRMixin, CliMixin, TickMixin
from .Signal import Signals

if TYPE_CHECKING:
    from factorio_circuit_ast.Network.DoubleNetwork import DoubleNetwork

ALIAS_CHARACTERS: Tuple[str, ...] = (*string.ascii_letters, *string.digits, "_")
nodes: Dict[int, ASTNode] = {}


class ASTNode(IRMixin, CliMixin, TickMixin, ABC):
    def __init__(
        self,
        name: str,
        output_network: Optional[DoubleNetwork] = None,
        nid: Optional[int] = None,
        alias: Optional[str] = None,
    ):
        self.name: str = name
        if alias:
            if any(char not in ALIAS_CHARACTERS for char in alias):
                raise ValueError(
                    f"invalid alias, only allowed characters are letters, numbers and _"
                )
        self.alias: Optional[str] = alias
        self.output_network: Optional[DoubleNetwork] = output_network
        if self.output_network:
            self.output_network.depends_on(self)
        self.previous_result: Optional[Signals] = None
        self.id = nid if nid is not None else max([*nodes.keys(), 0]) + 1
        nodes[self.id] = self

    @abstractmethod
    def _inner_to_ir(self) -> str:
        raise NotImplementedError

    def to_ir(self) -> str:
        res: str = f"id={self.id}"
        if self.alias:
            res += f" alias={self.alias}"
        return f"{res}:{self._inner_to_ir()}"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ASTNode):
            return (
                self.name == other.name and self.output_network == other.output_network
            )
        return False
