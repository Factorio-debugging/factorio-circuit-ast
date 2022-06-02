from abc import ABC, abstractmethod

from typing import Dict

from .Signal import Signal

Signals = Dict[Signal, int]


class ASTNode(ABC):
    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def output(self) -> Signals:
        raise NotImplementedError
