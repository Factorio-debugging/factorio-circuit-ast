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
        if isinstance(left, SignalOperand):
            if left.signal == Signal.SIGNAL_EACH:
                if isinstance(self.right, SignalOperand):
                    assert (
                        self.right.signal != Signal.SIGNAL_EACH
                    ), "Only one operand for Operation may be Each"
            else:
                assert (
                    left.signal in ConcreteSignal
                ), "Only concrete signals or Each are allowed in Operation"
                assert (
                    self.result.signal != Signal.SIGNAL_EACH
                    or isinstance(self.right, SignalOperand)
                    and self.right.signal == Signal.SIGNAL_EACH
                ), "Can not assign signal other than each to Operation while having result each"
        self._left = left

    @property
    def right(self) -> Operand:
        return self._right

    @right.setter
    def right(self, right: Operand) -> None:
        if isinstance(right, SignalOperand):
            if right.signal == Signal.SIGNAL_EACH:
                if isinstance(self.left, SignalOperand):
                    assert (
                        self.left.signal != Signal.SIGNAL_EACH
                    ), "Only one operand for Operation may be Each"
            else:
                assert (
                    right.signal in ConcreteSignal
                ), "Only concrete signals or Each are allowed in Operation"
            assert (
                self.result.signal != Signal.SIGNAL_EACH
                or isinstance(self.left, SignalOperand)
                and self.left.signal == Signal.SIGNAL_EACH
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
        if op.signal == Signal.SIGNAL_EACH:
            assert (
                isinstance(self.left, SignalOperand)
                and self.left.signal == Signal.SIGNAL_EACH
                or isinstance(self.right, SignalOperand)
                and self.right.signal == Signal.SIGNAL_EACH
            ), "Need to have one Operand as Each in order to set result to each"
        self._result = op
