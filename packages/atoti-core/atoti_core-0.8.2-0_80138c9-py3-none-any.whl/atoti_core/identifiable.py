from typing import Union

from .has_identifier import HasIdentifier, IdentifierT

Identifiable = Union[HasIdentifier[IdentifierT], IdentifierT]
