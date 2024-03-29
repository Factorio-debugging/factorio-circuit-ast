from __future__ import annotations

from enum import Enum
from typing import List
from weakref import ref, ReferenceType

import numpy as np

from factorio_circuit_ast.AST.ASTNode import ASTNode
from factorio_circuit_ast.AST.Signal import Signal, WildcardSignal, Signals


class NetworkType(Enum):
    RED = "red"
    GREEN = "green"


class Network:
    def __init__(self, nid: int, network_type: NetworkType) -> None:
        self.type: NetworkType = network_type
        self._depends: List[ReferenceType[ASTNode]] = []
        self._dependants: List[ReferenceType[ASTNode]] = []
        self._previous_state: Signals = {}
        self._current_state: Signals = {}
        self.id: int = nid

    def depends_on(self, node: ASTNode) -> None:
        self._depends.append(ref(node))

    def dependant_from(self, node: ASTNode) -> None:
        self._dependants.append(ref(node))

    def get_signal(self, signal: Signal) -> np.int32:
        assert (
            signal not in WildcardSignal
        ), f"only concrete signals are allowed in get_signal, got {signal}"
        return self._previous_state.setdefault(signal, np.int32(0))

    def get_signals(self) -> Signals:
        return self._previous_state

    def tick(self) -> None:
        self._previous_state = self._current_state
        self._current_state = {}

    def update_signal(self, signal: Signal, value: np.int32) -> None:
        assert (
            signal not in WildcardSignal
        ), f"only concrete signals are allowed in update_signal, got {signal}"
        self._current_state[signal] = (
            self._current_state.setdefault(signal, np.int32(0)) + value
        )

    def update_signals(self, signals: Signals) -> None:
        assert (
            Signal.SIGNAL_EACH not in signals
            and Signal.SIGNAL_EVERYTHING not in signals
            and Signal.SIGNAL_ANYTHING not in signals
        ), "only concrete signals are allowed in update_signals"
        self._current_state.update(signals)

    @property
    def depends(self) -> List[ReferenceType[ASTNode]]:
        return self._depends

    @property
    def dependants(self) -> List[ReferenceType[ASTNode]]:
        return self._dependants

    def __repr__(self) -> str:
        return f"Network(nid={self.id!r}, network={self.type!r})"

    def cli_repr(self) -> str:
        return f"n{self.id}"
