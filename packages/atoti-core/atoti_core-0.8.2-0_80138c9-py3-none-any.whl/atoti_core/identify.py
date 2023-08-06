from typing import Union

from .has_identifier import HasIdentifier, IdentifierT


def identify(
    identifiable: Union[HasIdentifier[IdentifierT], IdentifierT], /
) -> IdentifierT:
    return (
        identifiable._identifier
        if isinstance(identifiable, HasIdentifier)
        else identifiable
    )
