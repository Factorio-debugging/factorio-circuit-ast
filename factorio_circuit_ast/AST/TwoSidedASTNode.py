from abc import ABC
from typing import Optional, Any

import numpy as np

from factorio_circuit_ast.Network import DoubleNetwork
from .ASTNode import ASTNode
from .Operand import Operand, SignalOperand, ConstantOperand


class TwoSidedASTNode(ASTNode, ABC):
    def __init__(
        self,
        name: str,
        output_network: Optional[DoubleNetwork] = None,
        input_network: Optional[DoubleNetwork] = None,
        nid: Optional[int] = None,
        alias: Optional[str] = None,
    ):
        super().__init__(name, output_network, nid, alias)
        self.input_network: Optional[DoubleNetwork] = input_network
        if self.input_network:
            self.input_network.dependant_from(self)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, TwoSidedASTNode):
            return super().__eq__(other) and self.input_network == other.input_network
        return False  # pragma: no cover

    def _get_input_value(self, op: Operand) -> np.int32:
        if isinstance(op, SignalOperand):
            assert self.input_network
            return self.input_network.get_signal(op.signal)
        elif isinstance(op, ConstantOperand):
            return op.constant
        raise NotImplementedError(f"Invalid operand {op}")
