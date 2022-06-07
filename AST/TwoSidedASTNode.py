from abc import ABC
from typing import Optional, Any

from .ASTNode import ASTNode
from .DoubleNetwork import DoubleNetwork


class TwoSidedASTNode(ASTNode, ABC):
    def __init__(
        self,
        name: str,
        output_network: Optional[DoubleNetwork] = None,
        input_network: Optional[DoubleNetwork] = None,
    ):
        super().__init__(name, output_network)
        self.input_network: Optional[DoubleNetwork] = input_network

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, TwoSidedASTNode):
            return super().__eq__(other) and self.input_network == other.input_network
        return False  # pragma: no cover
