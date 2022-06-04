from abc import ABC, abstractmethod
from typing import Optional

from .Signal import Signals


class ASTNode(ABC):
    def __init__(self, name: str):
        self.name: str = name
        self.previous_result: Optional[Signals] = None

    @abstractmethod
    def tick(self) -> None:
        raise NotImplementedError
