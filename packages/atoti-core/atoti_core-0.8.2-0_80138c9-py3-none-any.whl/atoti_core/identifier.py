from abc import ABC, abstractmethod
from functools import cached_property


class Identifier(ABC):
    @property
    @abstractmethod
    def key(self) -> tuple[str, ...]:
        ...

    @cached_property
    def java_description(self) -> str:
        return "@".join(reversed(self.key))

    def __str__(self) -> str:
        return str(self.key)
