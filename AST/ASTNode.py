from abc import ABC, abstractmethod

import numpy as np
from typing import Dict

from .Signal import Signal

Signals = Dict[Signal, np.int32]


class ASTNode(ABC):
    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def output(self) -> Signals:
        raise NotImplementedError
