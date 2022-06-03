from enum import Enum

import numpy as np
from typing import Optional, Any

from .ASTNode import ASTNode, Signals
from .Operand import Operand, ConstantOperand, SignalOperand
from .Signal import Signal, ConcreteSignal


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

    def calculate(self, left: np.int32, right: np.int32) -> np.int32:
        if self == NumericOperator.ADD:
            return left + right
        elif self == NumericOperator.SUBTRACT:
            return left - right
        elif self == NumericOperator.MULTIPLY:
            return left * right
        elif self == NumericOperator.DIVIDE:
            return left // right
        elif self == NumericOperator.MODULO:
            return left % right
        elif self == NumericOperator.EXPONENT:
            return left**right
        elif self == NumericOperator.LEFT_BIT_SHIFT:
            return left << right
        elif self == NumericOperator.RIGHT_BIT_SHIFT:
            return left >> right
        elif self == NumericOperator.AND:
            return left & right
        elif self == NumericOperator.OR:
            return left | right
        elif self == NumericOperator.XOR:
            return left ^ right
        raise NotImplementedError(f"Unknown operator {self}")


class Operation(ASTNode):
    def __init__(
        self,
        operation: NumericOperator,
        result: SignalOperand,
        left: Optional[Operand] = None,
        right: Optional[Operand] = None,
    ):
        super().__init__("Operation")
        self.operation: NumericOperator = operation
        self._left: Operand
        self._right: Operand
        self._result: SignalOperand
        self.result = result
        self.left = left if left else ConstantOperand(np.int32(0))
        self.right = right if right else ConstantOperand(np.int32(0))

    def output(self) -> Signals:
        raise NotImplementedError("")

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Operation):
            return (
                self.operation == other.operation
                and self.right == other.right
                and self.left == other.left
                and self.result == other.result
            )
        return False

    def __repr__(self) -> str:
        return f"Operation(operation={self.operation}, left={self.left}, right={self.right})"

    @property
    def left(self) -> Operand:
        return self._left

    @left.setter
    def left(self, left: Operand) -> None:
        if left.is_each():
            assert (
                not self.right.is_each()
            ), "Only one operand for Operation may be Each"
        elif left.abstract():
            raise AssertionError(
                "Only concrete signals or Each are allowed in Operation"
            )
        else:
            assert (
                not self.result.is_each() or self.right.is_each()
            ), "Can not assign signal other than each to Operation while having result each"
        self._left = left

    @property
    def right(self) -> Operand:
        return self._right

    @right.setter
    def right(self, right: Operand) -> None:
        if right.is_each():
            assert not self.left.is_each(), "Only one operand for Operation may be Each"
        elif right.abstract():
            raise AssertionError(
                "Only concrete signals or Each are allowed in Operation"
            )
        else:
            assert (
                not self.result.is_each() or self.left.is_each()
            ), "Can not assign signal other than each to Operation while having result each"
        self._right = right

    @property
    def result(self) -> SignalOperand:
        return self._result

    @result.setter
    def result(self, op: SignalOperand) -> None:
        assert op.signal not in (
            Signal.SIGNAL_EVERYTHING,
            Signal.SIGNAL_ANYTHING,
        ), "Anything or Everything are not allowed as Operation results"
        if op.is_each():
            assert (
                self.left.is_each() or self.right.is_each()
            ), "Need to have one Operand as Each in order to set result to each"
        self._result = op
