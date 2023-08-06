from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .identifier import Identifier

IdentifierT = TypeVar("IdentifierT", bound=Identifier, covariant=True)


class HasIdentifier(Generic[IdentifierT], ABC):
    @property
    @abstractmethod
    def _identifier(self) -> IdentifierT:
        ...


HasIdentifierBound = HasIdentifier[Identifier]
