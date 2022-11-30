from abc import abstractmethod


class IRMixin:
    @abstractmethod
    def to_ir(self) -> str:
        raise NotImplementedError
