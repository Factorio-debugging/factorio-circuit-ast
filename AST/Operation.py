from enum import Enum
from typing import Optional, Any

import numpy as np

from .DoubleNetwork import DoubleNetwork
from .Operand import Operand, ConstantOperand, SignalOperand
from .Signal import Signal, Signals
from .TwoSidedASTNode import TwoSidedASTNode


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


class Operation(TwoSidedASTNode):
    def __init__(
        self,
        operation: NumericOperator,
        result: SignalOperand,
        output_network: Optional[DoubleNetwork] = None,
        input_network: Optional[DoubleNetwork] = None,
        left: Optional[Operand] = None,
        right: Optional[Operand] = None,
        nid: Optional[int] = None,
    ):
        super().__init__("Operation", output_network, input_network, nid)
        self.operation: NumericOperator = operation
        # set these for comparison
        self._left: Operand = left if left else ConstantOperand(np.int32(0))
        self._right: Operand = right if right else ConstantOperand(np.int32(0))
        self._result: SignalOperand = result
        # and set them with checks
        self.result = result
        self.left = self._left
        self.right = self._right

    @property
    def left(self) -> Operand:
        return self._left

    @left.setter
    def left(self, left: Operand) -> None:
        if left and isinstance(left, SignalOperand):
            assert self.input_network, "can not set signal without network"
        if left.is_each():
            assert (
                not self.right.is_each()
            ), "Only one operand for Operation may be Each"
        elif left.wildcard():
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
        if right and isinstance(right, SignalOperand):
            assert self.input_network, "can not set signal without network"
        if right.is_each():
            assert not self.left.is_each(), "Only one operand for Operation may be Each"
        elif right.wildcard():
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

    def tick(self) -> None:
        results: Signals = {}
        if not (self.left.is_each() or self.right.is_each()):
            assert (
                not self.result.is_each()
            ), "result is each, but neither left nor right are each"
            results[self.result.signal] = self.operation.calculate(
                self._get_input_value(self.left),
                self._get_input_value(self.right),
            )
        else:
            assert self.input_network
            if self.left.is_each():
                assert self.input_network
                for signal, value in self.input_network.get_signals().items():
                    results[signal] = self.operation.calculate(
                        value, self._get_input_value(self.right)
                    )
            elif self.right.is_each():
                for signal, value in self.input_network.get_signals().items():
                    results[signal] = self.operation.calculate(
                        self._get_input_value(self.left), value
                    )
            else:
                raise NotImplementedError("unreachable")
        if self.output_network:
            if self.result.is_each():
                for signal, value in results.items():
                    self.output_network.update_signal(signal, value)
            else:
                self.output_network.update_signal(
                    self.result.signal, np.sum([*results.values()], dtype=np.int32)
                )
        self.previous_result = results

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Operation):
            return (
                super().__eq__(other)
                and self.operation == other.operation
                and self.right == other.right
                and self.left == other.left
                and self.result == other.result
            )
        return False

    def __repr__(self) -> str:
        return (
            f"Operation("
            f"operation={self.operation}, "
            f"result={self.result}, "
            f"output_network={self.output_network}, "
            f"input_network={self.input_network}, "
            f"left={self.left}, "
            f"right={self.right})"
        )
