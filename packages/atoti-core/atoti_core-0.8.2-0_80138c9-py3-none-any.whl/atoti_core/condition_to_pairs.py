from typing import Literal, Optional, cast

from .decombine_condition import decombine_condition
from .operation import (
    ComparisonCondition,
    Condition,
    ConditionSubjectT,
    ConditionTargetT,
)


def condition_to_pairs(
    condition: Condition[
        ConditionSubjectT,
        Literal["eq"],
        ConditionTargetT,
        Optional[Literal["and"]],
    ],
    /,
) -> list[tuple[ConditionSubjectT, ConditionTargetT]]:
    comparison_conditions = cast(
        tuple[
            ComparisonCondition[ConditionSubjectT, Literal["eq"], ConditionTargetT], ...
        ],
        decombine_condition(
            condition,
            allowed_comparison_operators=("eq",),
            allowed_combination_operators=("and",),
            allowed_isin_element_types=(),
        )[0][0],
    )
    return [
        (condition.subject, condition.target) for condition in comparison_conditions
    ]
