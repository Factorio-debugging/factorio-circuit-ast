from abc import ABC, abstractmethod


class TickMixin(ABC):
    @abstractmethod
    def tick(self) -> None:
        raise NotImplementedError
