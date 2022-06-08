from enum import Enum
from typing import Optional, Any

import numpy as np

from .DoubleNetwork import DoubleNetwork
from .Operand import Operand, SignalOperand, ConstantOperand
from .Signal import Signal
from .TwoSidedASTNode import TwoSidedASTNode


class DeciderOperator(Enum):
    GREATER_THAN: str = ">"
    LESS_THAN: str = "<"
    GREATER_OR_EQUAL: str = ">="
    LESS_OR_EQUAL: str = "<="
    EQUAL: str = "="
    NOT_EQUAL: str = "!="

    def calculate(self, left: np.int32, right: np.int32) -> np.int32:
        result: np.bool_
        if self == DeciderOperator.GREATER_THAN:
            result = left > right
        elif self == DeciderOperator.LESS_THAN:
            result = left < right
        elif self == DeciderOperator.GREATER_OR_EQUAL:
            result = left >= right
        elif self == DeciderOperator.LESS_OR_EQUAL:
            result = left <= right
        elif self == DeciderOperator.EQUAL:
            result = left == right
        elif self == DeciderOperator.NOT_EQUAL:
            result = left != right
        else:
            raise NotImplementedError(f"Unknown operator {self}")
        return np.int32(result)


class Comparison(TwoSidedASTNode):
    def __init__(
        self,
        operation: DeciderOperator,
        result: SignalOperand,
        output_network: Optional[DoubleNetwork] = None,
        input_network: Optional[DoubleNetwork] = None,
        left: Optional[Operand] = None,
        right: Optional[Operand] = None,
        copy_count_from_input: bool = True,
    ):
        super().__init__("Comparison", output_network, input_network)
        self.operation: DeciderOperator = operation
        self._result: SignalOperand = result
        self._left: Operand = left if left else ConstantOperand(np.int32(0))
        self._right: Operand = right if right else ConstantOperand(np.int32(0))
        self.result = result
        self.left = self._left
        self.right = self._right
        self.copy_count_from_input: bool = copy_count_from_input

    @property
    def left(self) -> Operand:
        return self._left

    @left.setter
    def left(self, left: Operand) -> None:
        if left and isinstance(left, SignalOperand):
            assert self.input_network, "can not set signal without network"
        if left.wildcard():
            if left.is_everything():
                assert not (
                    self.result.is_each() or self.result.is_anything()
                ), "everything wildcard needs everything concrete value as result"
            elif left.is_anything():
                assert (
                    not self.result.is_each()
                ), "anything wildcard needs anything, everything or concrete signal as result"
            elif left.is_each():
                assert not (
                    self.result.is_anything() or self.result.is_everything()
                ), "each wildcard needs each or concrete signal as result"
            else:
                raise NotImplementedError(f"Unknown wildcard signal {left}")
        else:
            assert not (
                self.result.is_each() or self.result.is_anything()
            ), "concrete signal needs everything or concrete signal as result"
        self._left = left

    @property
    def right(self) -> Operand:
        return self._right

    @right.setter
    def right(self, right: Operand) -> None:
        assert (
            not right.wildcard()
        ), "right side of comparison is not allowed to be a wildcard"
        if right and isinstance(right, SignalOperand):
            assert self.input_network, "can not set signal without network"
        self._right = right

    @property
    def result(self) -> SignalOperand:
        return self._result

    @result.setter
    def result(self, op: SignalOperand) -> None:
        if op.wildcard():
            assert (
                self.input_network
            ), "can not use result wildcards without input network"
            if op.is_everything():
                assert (
                    not self.left.is_each()
                ), "everything wildcard may not be the result of each"
            elif op.is_anything():
                assert (
                    self.left.is_anything()
                ), "anything wildcard needs anything signal on the left side"
            elif op.is_each():
                assert (
                    self.left.is_each()
                ), "each wildcard needs each signal on the left side"
            else:
                raise NotImplementedError(f"Unknown wildcard signal {op}")
        self._result = op

    def _get_input_value(self, op: Operand) -> np.int32:
        if isinstance(op, SignalOperand):
            assert self.input_network
            return self.input_network.get_signal(op.signal)
        elif isinstance(op, ConstantOperand):
            return op.constant
        raise NotImplementedError(f"Invalid operand {op}")

    def tick(self) -> None:
        self.previous_result = {}
        right_value: np.int32 = self._get_input_value(self.right)
        if self.left.is_each():
            assert self.input_network
            for key, value in self.input_network.get_signals().items():
                if self.operation.calculate(value, right_value):
                    self.previous_result[key] = (
                        value if self.copy_count_from_input else np.int32(1)
                    )
            if not self.result.is_each() and self.previous_result:
                self.previous_result = {
                    self.result.signal: np.sum(
                        [*self.previous_result.values()], dtype=np.int32
                    )
                }
        else:
            passed: bool = False
            right_signal: Optional[Signal] = (
                right.signal if isinstance(right := self.right, SignalOperand) else None
            )
            if self.left.is_anything():
                assert self.input_network
                for key, value in self.input_network.get_signals().items():
                    if right_signal and key == right_signal:
                        continue
                    if self.operation.calculate(value, right_value):
                        self.previous_result = {
                            key: value if self.copy_count_from_input else np.int32(1)
                        }
                        passed = True
                        break
            elif self.left.is_everything():
                assert self.input_network
                passed = True
                for key, value in self.input_network.get_signals().items():
                    if right_signal and key == right_signal:
                        continue
                    if not self.operation.calculate(value, right_value):
                        passed = False
                        break
            else:
                passed = bool(
                    self.operation.calculate(
                        self._get_input_value(self.left),
                        right_value,
                    )
                )
            if passed and self.input_network:
                if self.result.is_everything():
                    self.previous_result = {
                        key: value if self.copy_count_from_input else np.int32(1)
                        for key, value in self.input_network.get_signals().items()
                        if value != 0
                    }
                elif not self.result.is_anything():
                    self.previous_result = {
                        self.result.signal: self._get_input_value(self.result)
                        if self.copy_count_from_input
                        else np.int32(1)
                    }
            elif passed:
                if not self.result.is_everything() and not self.copy_count_from_input:
                    self.previous_result = {self.result.signal: np.int32(1)}
        if self.output_network:
            self.output_network.update_signals(self.previous_result)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Comparison):
            return (
                super().__eq__(other)
                and self.operation == other.operation
                and self.right == other.right
                and self.left == other.left
                and self.result == other.result
                and self.copy_count_from_input == other.copy_count_from_input
            )
        return False

    def __repr__(self) -> str:
        return (
            f"Comparison("
            f"operation={self.operation}, "
            f"result={self.result}, "
            f"output_network={self.output_network}, "
            f"input_network={self.input_network}, "
            f"left={self.left}, "
            f"right={self.right}, "
            f"copy_count_from_input={self.copy_count_from_input})"
        )
