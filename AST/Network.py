from __future__ import annotations
from weakref import ref, ReferenceType

from typing import List, Dict, Optional

from .ASTNode import ASTNode, Signals
from .Signal import Signal


networks: Dict[int, ReferenceType[Network]] = {}


class Network:
    def __init__(self, nid: Optional[int] = None) -> None:
        self._depends: List[ReferenceType[ASTNode]] = []
        self._dependants: List[ReferenceType[ASTNode]] = []
        self._previous_state: Signals = {}
        self._current_state: Signals = {}
        self.id = nid if nid is not None else max([*networks.keys(), 0]) + 1
        networks[self.id] = ref(self)

    def depends_on(self, node: ASTNode) -> None:
        self._depends.append(ref(node))

    def dependant_from(self, node: ASTNode) -> None:
        self._dependants.append(ref(node))

    def get_signal_value(self, signal: Signal) -> int:
        return self._previous_state.setdefault(signal, 0)

    def get_all_values(self) -> Signals:
        return self._previous_state

    def tick(self) -> None:
        self._previous_state = self._current_state
        self._current_state = {}

    def update_value(self, signal: Signal, value: int) -> None:
        self._current_state[signal] = self._current_state.setdefault(signal, 0) + value

    @property
    def depends(self) -> List[ReferenceType[ASTNode]]:
        return self._depends

    @property
    def dependants(self) -> List[ReferenceType[ASTNode]]:
        return self._dependants
