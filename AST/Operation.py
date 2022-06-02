from enum import Enum

from typing import Optional, Any

from .ASTNode import ASTNode, Signals
from .Operand import Operand, ConstantOperand


class NumericOperator(Enum):
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    EXPONENT = "^"
    LEFT_BIT_SHIFT = "<<"
    RIGHT_BIT_SHIFT = ">>"
    AND = "AND"
    OR = "OR"
    XOR = "XOR"


class Operation(ASTNode):
    def __init__(
        self,
        operation: NumericOperator,
        left: Optional[Operand] = None,
        right: Optional[Operand] = None,
    ):
        super().__init__("Operation")
        self.operation: NumericOperator = operation
        self.left: Operand = left if left else ConstantOperand(0)
        self.right: Operand = right if right else ConstantOperand(0)

    def output(self) -> Signals:
        raise NotImplementedError("")

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Operation):
            return (
                self.operation == other.operation
                and self.right == other.right
                and self.left == other.left
            )
        return False

    def __repr__(self) -> str:
        return f"Operation(operation={self.operation}, left={self.left}, right={self.right})"
