from typing import Union

from .has_identifier import HasIdentifier, IdentifierT

IdentifierLike = Union[HasIdentifier[IdentifierT], IdentifierT]
