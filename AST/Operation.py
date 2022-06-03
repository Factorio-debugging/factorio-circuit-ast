from enum import Enum
from typing import Optional, Any

import numpy as np

from .ASTNode import ASTNode
from .Operand import Operand, ConstantOperand, SignalOperand
from .Signal import Signal


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
        # set these for comparison
        self._left: Operand = left if left else ConstantOperand(np.int32(0))
        self._right: Operand = right if right else ConstantOperand(np.int32(0))
        self._result: SignalOperand = result
        # and set them with checks
        self.result = result
        self.left = self._left
        self.right = self._right

    def tick(self) -> None:
        if not (self.left.is_each() or self.right.is_each()):
            self.result.update_self(
                self.operation.calculate(self.left.value(), self.right.value())
            )
        else:
            assert (result_net := self.result.network)
            if self.result.is_each():
                if self.left.is_each():
                    assert isinstance(self.left, SignalOperand) and (
                        left_net := self.left.network
                    )
                    for signal, value in left_net.get_all_values().items():
                        result_net.update_value(
                            signal, self.operation.calculate(value, self.right.value())
                        )
                elif self.right.is_each():
                    assert isinstance(self.right, SignalOperand) and (
                        right_net := self.right.network
                    )
                    for signal, value in right_net.get_all_values().items():
                        result_net.update_value(
                            signal, self.operation.calculate(self.left.value(), value)
                        )
                else:
                    raise AssertionError(
                        "result is each, but neither left nor right are each"
                    )

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
