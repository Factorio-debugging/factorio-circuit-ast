from abc import ABC, abstractmethod
from typing import Any, Optional
from weakref import ref, ReferenceType

import numpy as np

from .Network import Network
from .Signal import Signal, AbstractSignal


class Operand(ABC):
    @abstractmethod
    def value(self) -> np.int32:
        raise NotImplementedError

    @abstractmethod
    def abstract(self) -> bool:
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
    def __init__(self, network: Network, signal: Signal):
        self.network = network
        self.signal: Signal = signal

    def value(self) -> np.int32:
        if network := self.network:
            return network.get_signal_value(self.signal)
        raise RuntimeError("Network belonging to signal has been destroyed")

    def abstract(self) -> bool:
        return self.signal in AbstractSignal

    def is_each(self) -> bool:
        return self.signal == Signal.SIGNAL_EACH

    def is_anything(self) -> bool:
        return self.signal == Signal.SIGNAL_ANYTHING

    def is_everything(self) -> bool:
        return self.signal == Signal.SIGNAL_EVERYTHING

    def update_self(self, value: np.int32) -> None:
        assert (
            self.signal not in AbstractSignal
        ), "Can not use update self on abstract signals"
        if network := self.network:
            network.update_value(self.signal, value)
        else:
            raise RuntimeError("Network belonging to signal has been destroyed")

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, SignalOperand):
            return self.network == other.network and self.signal == other.signal
        return False

    def __repr__(self) -> str:
        return f"SignalOperand(network={self.network!r}, signal={self.signal!r})"

    @property
    def network(self) -> Optional[Network]:
        return self._network()

    @network.setter
    def network(self, net: Network) -> None:
        self._network: ReferenceType[Network] = ref(net)


class ConstantOperand(Operand):
    def __init__(self, constant: np.int32):
        self.constant: np.int32 = constant

    def value(self) -> np.int32:
        return self.constant

    def abstract(self) -> bool:
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
