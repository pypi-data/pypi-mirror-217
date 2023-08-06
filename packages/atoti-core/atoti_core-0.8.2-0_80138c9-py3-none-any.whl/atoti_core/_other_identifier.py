from typing import TypeVar

from .identifier import Identifier

OtherIdentifierT = TypeVar("OtherIdentifierT", bound=Identifier, covariant=True)
