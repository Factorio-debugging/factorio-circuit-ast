from abc import ABC


class CliMixin(ABC):
    def cli_repr(self) -> str:
        raise NotImplementedError
