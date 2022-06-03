from abc import ABC, abstractmethod
from typing import Dict

import numpy as np

from .Signal import Signal

Signals = Dict[Signal, np.int32]


class ASTNode(ABC):
    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def tick(self) -> None:
        raise NotImplementedError
