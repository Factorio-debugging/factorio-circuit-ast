from abc import ABC, abstractmethod
from typing import Any

import numpy as np

from .Signal import Signal, WildcardSignal


class Operand(ABC):
    @abstractmethod
    def wildcard(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_each(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_anything(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_everything(self) -> bool:
        raise NotImplementedError


class SignalOperand(Operand):
    def __init__(self, signal: Signal):
        self.signal: Signal = signal

    def wildcard(self) -> bool:
        return self.signal in WildcardSignal

    def is_each(self) -> bool:
        return self.signal == Signal.SIGNAL_EACH

    def is_anything(self) -> bool:
        return self.signal == Signal.SIGNAL_ANYTHING

    def is_everything(self) -> bool:
        return self.signal == Signal.SIGNAL_EVERYTHING

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, SignalOperand):
            return self.signal == other.signal
        return False

    def __repr__(self) -> str:
        return f"SignalOperand(signal={self.signal!r})"


class ConstantOperand(Operand):
    def __init__(self, constant: np.int32):
        self.constant: np.int32 = constant

    def wildcard(self) -> bool:
        return False

    def is_each(self) -> bool:
        return False

    def is_anything(self) -> bool:
        return False

    def is_everything(self) -> bool:
        return False

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ConstantOperand):
            return self.constant == other.constant
        return False

    def __repr__(self) -> str:
        return f"ConstantOperand(constant={self.constant})"
