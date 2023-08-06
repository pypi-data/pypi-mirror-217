from typing import Literal, Optional

from .condition_to_pairs import condition_to_pairs
from .has_identifier import IdentifierT
from .operation import Condition, ConditionTargetT


def condition_to_dict(
    condition: Condition[
        IdentifierT,
        Literal["eq"],
        ConditionTargetT,
        Optional[Literal["and"]],
    ],
    /,
) -> dict[IdentifierT, ConditionTargetT]:
    pairs = condition_to_pairs(condition)
    result: dict[IdentifierT, ConditionTargetT] = {}

    for identifier, target in pairs:
        if identifier in result:
            raise ValueError(
                f"Expected the combined condition to have distinct subjects but got `{identifier}` twice."
            )

        result[identifier] = target

    return result
