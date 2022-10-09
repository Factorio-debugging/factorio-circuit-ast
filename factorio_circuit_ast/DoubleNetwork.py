from typing import Optional, Any

import numpy as np

from .ASTNode import ASTNode
from .Network import Network, NetworkType
from .Signal import Signal, WildcardSignal, Signals


class DoubleNetwork:
    def __init__(
        self, red: Optional[Network] = None, green: Optional[Network] = None
    ) -> None:
        self.red = red
        self.green = green

    def get_signal(self, signal: Signal) -> np.int32:
        assert signal not in WildcardSignal
        return (self.red.get_signal(signal) if self.red else np.int32(0)) + (
            self.green.get_signal(signal) if self.green else np.int32(0)
        )

    def get_signals(self) -> Signals:
        result: Signals = self.red.get_signals() if self.red else {}
        if self.green:
            for signal, value in self.green.get_signals().items():
                result[signal] = result.setdefault(signal, np.int32(0)) + value
        return result

    def update_signal(self, signal: Signal, value: np.int32) -> None:
        assert signal not in WildcardSignal
        if self.red:
            self.red.update_signal(signal, value)
        if self.green:
            self.green.update_signal(signal, value)

    def update_signals(self, signals: Signals) -> None:
        assert (
            Signal.SIGNAL_EACH not in signals
            and Signal.SIGNAL_EVERYTHING not in signals
            and Signal.SIGNAL_ANYTHING not in signals
        ), "only concrete signals are allowed in update_signals"
        if self.red:
            self.red.update_signals(signals)
        if self.green:
            self.green.update_signals(signals)

    @property
    def red(self) -> Optional[Network]:
        return self._red

    @red.setter
    def red(self, net: Optional[Network]) -> None:
        if net and net.type != NetworkType.RED:
            raise TypeError("Can not assign green network to red DoubleNetwork part")
        self._red = net

    @property
    def green(self) -> Optional[Network]:
        return self._green

    @green.setter
    def green(self, net: Optional[Network]) -> None:
        if net and net.type != NetworkType.GREEN:
            raise TypeError("Can not assign green network to red DoubleNetwork part")
        self._green = net

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, DoubleNetwork):
            return self.red == other.red and self.green == other.green
        return False

    def __repr__(self) -> str:
        return f"DoubleNetwork(red={self.red!r}, green={self.green!r})"

    def cli_repr(self) -> str:
        return f"[r={self.red.cli_repr() if self.red else '-'},g={self.green.cli_repr() if self.green else '-'}]"

    def dependant_from(self, dependant: ASTNode) -> None:
        if self.red:
            self.red.dependant_from(dependant)
        if self.green:
            self.green.dependant_from(dependant)

    def depends_on(self, depends: ASTNode) -> None:
        if self.red:
            self.red.depends_on(depends)
        if self.green:
            self.green.depends_on(depends)

    def ir_repr(self, pre: str) -> str:
        res = ""
        if self.red:
            res += f"{pre}r={self.red.id} "
        if self.green:
            res += f"{pre}g={self.green.id} "
        return res
