from abc import ABC, abstractmethod


class CliMixin(ABC):
    @abstractmethod
    def cli_repr(self) -> str:
        raise NotImplementedError
