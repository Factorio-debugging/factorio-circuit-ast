from typing import Optional

from .ASTNode import ASTNode
from .DoubleNetwork import DoubleNetwork
from .Signal import Signals, WildcardSignal


class Constant(ASTNode):
    def __init__(
        self,
        output_network: Optional[DoubleNetwork] = None,
        signals: Optional[Signals] = None,
        is_on: bool = True,
        nid: Optional[int] = None,
        alias: Optional[str] = None,
    ):
        super().__init__("Constant", output_network, nid, alias)
        self.signals = signals if signals else {}
        self.is_on: bool = is_on

    @property
    def signals(self) -> Signals:
        return self._signals

    @signals.setter
    def signals(self, signal: Signals) -> None:
        assert all(
            sig not in signal.keys() for sig in WildcardSignal
        ), "can not set constant to wildcard signal"
        self._signals = signal

    def tick(self) -> None:
        self.previous_result = {}
        if self.is_on:
            self.previous_result = self.signals
            if self.output_network:
                self.output_network.update_signals(self.previous_result)

    def cli_repr(self) -> str:
        return (
            f"Constant "
            f"output={self.output_network.cli_repr() if self.output_network else '-'} "
            f"[{', '.join(f'{sig.value}: {value}' for sig, value in self.signals.items())}] "
            f"({'on' if self.is_on else 'off'})"
        )

    def _inner_to_ir(self) -> str:
        res: str = "const "
        if self.is_on:
            res += "on "
        for sig, num in self.signals.items():
            res += f"sig={sig.value}={num} "
        if self.output_network:
            res += self.output_network.ir_repr("out")
        return res[:-1]
