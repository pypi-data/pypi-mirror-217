from __future__ import annotations

from typing import Literal, Union, overload

from ._other_identifier import OtherIdentifierT
from .constant import Constant, ConstantValue
from .has_identifier import HasIdentifier, IdentifierT
from .operation import (
    ComparisonCondition,
    Condition,
    OperandConvertible,
    Operation,
    convert_to_operand,
)


class OperandConvertibleWithIdentifier(
    OperandConvertible[IdentifierT],
    HasIdentifier[IdentifierT],
):
    """This class overrides `OperandConvertible`'s `Condition`-creating methods so that the type of the returned `Condition`'s `subject` is narrowed down to an instance of `Identifier` instead of a `Union[Identifier, Operation]`.

    The returned `Condition`'s `target` is also kept as narrow as possible thanks to `@overload`s.
    """

    # Without this, the classes inheriting from this class are considered unhashable.
    def __hash__(self) -> int:
        return super().__hash__()

    def isnull(
        self,
    ) -> Condition[IdentifierT, Literal["eq"], None, None]:
        return ComparisonCondition(
            subject=self._operation_operand,
            operator="eq",
            target=None,
        )

    @property
    def _operation_operand(self) -> IdentifierT:
        return self._identifier

    # The signature is not compatible with `object.__eq__()` on purpose.
    @overload  # type: ignore[override]
    def __eq__(
        self, other: ConstantValue, /
    ) -> Condition[IdentifierT, Literal["eq"], Constant, None]:
        ...

    @overload
    def __eq__(
        self, other: HasIdentifier[OtherIdentifierT], /
    ) -> Condition[IdentifierT, Literal["eq"], OtherIdentifierT, None]:
        ...

    @overload
    def __eq__(
        self,
        other: Union[
            ConstantValue,
            HasIdentifier[OtherIdentifierT],
            Operation[OtherIdentifierT],
        ],
        /,
    ) -> Condition[
        IdentifierT,
        Literal["eq"],
        Union[Constant, OtherIdentifierT, Operation[OtherIdentifierT]],
        None,
    ]:
        ...

    # The signature is not compatible with `object.__eq__()` on purpose.
    def __eq__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: Union[
            ConstantValue,
            HasIdentifier[OtherIdentifierT],
            Operation[OtherIdentifierT],
        ],
        /,
    ) -> Condition[
        IdentifierT,
        Literal["eq"],
        Union[Constant, OtherIdentifierT, Operation[OtherIdentifierT]],
        None,
    ]:
        assert other is not None, "Use `isnull()` instead."
        return ComparisonCondition(
            subject=self._operation_operand,
            target=convert_to_operand(other),
            operator="eq",
        )

    @overload
    def __ge__(
        self, other: ConstantValue, /
    ) -> Condition[IdentifierT, Literal["ge"], Constant, None]:
        ...

    @overload
    def __ge__(
        self, other: HasIdentifier[OtherIdentifierT], /
    ) -> Condition[IdentifierT, Literal["ge"], OtherIdentifierT, None]:
        ...

    @overload
    def __ge__(
        self,
        other: Union[
            ConstantValue,
            HasIdentifier[OtherIdentifierT],
            Operation[OtherIdentifierT],
        ],
        /,
    ) -> Condition[
        IdentifierT,
        Literal["ge"],
        Union[Constant, OtherIdentifierT, Operation[OtherIdentifierT]],
        None,
    ]:
        ...

    def __ge__(
        self,
        other: Union[
            ConstantValue,
            HasIdentifier[OtherIdentifierT],
            Operation[OtherIdentifierT],
        ],
        /,
    ) -> Condition[
        IdentifierT,
        Literal["ge"],
        Union[Constant, OtherIdentifierT, Operation[OtherIdentifierT]],
        None,
    ]:
        return ComparisonCondition(
            subject=self._operation_operand,
            operator="ge",
            target=convert_to_operand(other),
        )

    @overload
    def __gt__(
        self, other: ConstantValue, /
    ) -> Condition[IdentifierT, Literal["gt"], Constant, None]:
        ...

    @overload
    def __gt__(
        self, other: HasIdentifier[OtherIdentifierT], /
    ) -> Condition[IdentifierT, Literal["gt"], OtherIdentifierT, None]:
        ...

    @overload
    def __gt__(
        self,
        other: Union[
            ConstantValue,
            HasIdentifier[OtherIdentifierT],
            Operation[OtherIdentifierT],
        ],
        /,
    ) -> Condition[
        IdentifierT,
        Literal["gt"],
        Union[Constant, OtherIdentifierT, Operation[OtherIdentifierT]],
        None,
    ]:
        ...

    def __gt__(
        self,
        other: Union[
            ConstantValue,
            HasIdentifier[OtherIdentifierT],
            Operation[OtherIdentifierT],
        ],
        /,
    ) -> Condition[
        IdentifierT,
        Literal["gt"],
        Union[Constant, OtherIdentifierT, Operation[OtherIdentifierT]],
        None,
    ]:
        return ComparisonCondition(
            subject=self._operation_operand,
            operator="gt",
            target=convert_to_operand(other),
        )

    @overload
    def __le__(
        self, other: ConstantValue, /
    ) -> Condition[IdentifierT, Literal["le"], Constant, None]:
        ...

    @overload
    def __le__(
        self, other: HasIdentifier[OtherIdentifierT], /
    ) -> Condition[IdentifierT, Literal["le"], OtherIdentifierT, None]:
        ...

    @overload
    def __le__(
        self,
        other: Union[
            ConstantValue,
            HasIdentifier[OtherIdentifierT],
            Operation[OtherIdentifierT],
        ],
        /,
    ) -> Condition[
        IdentifierT,
        Literal["le"],
        Union[Constant, OtherIdentifierT, Operation[OtherIdentifierT]],
        None,
    ]:
        ...

    def __le__(
        self,
        other: Union[
            ConstantValue,
            HasIdentifier[OtherIdentifierT],
            Operation[OtherIdentifierT],
        ],
        /,
    ) -> Condition[
        IdentifierT,
        Literal["le"],
        Union[Constant, OtherIdentifierT, Operation[OtherIdentifierT]],
        None,
    ]:
        return ComparisonCondition(
            subject=self._operation_operand,
            operator="le",
            target=convert_to_operand(other),
        )

    @overload
    def __lt__(
        self, other: ConstantValue, /
    ) -> Condition[IdentifierT, Literal["lt"], Constant, None]:
        ...

    @overload
    def __lt__(
        self, other: HasIdentifier[OtherIdentifierT], /
    ) -> Condition[IdentifierT, Literal["lt"], OtherIdentifierT, None]:
        ...

    @overload
    def __lt__(
        self,
        other: Union[
            ConstantValue,
            HasIdentifier[OtherIdentifierT],
            Operation[OtherIdentifierT],
        ],
        /,
    ) -> Condition[
        IdentifierT,
        Literal["lt"],
        Union[Constant, OtherIdentifierT, Operation[OtherIdentifierT]],
        None,
    ]:
        ...

    def __lt__(
        self,
        other: Union[
            ConstantValue,
            HasIdentifier[OtherIdentifierT],
            Operation[OtherIdentifierT],
        ],
        /,
    ) -> Condition[
        IdentifierT,
        Literal["lt"],
        Union[Constant, OtherIdentifierT, Operation[OtherIdentifierT]],
        None,
    ]:
        return ComparisonCondition(
            subject=self._operation_operand,
            operator="lt",
            target=convert_to_operand(other),
        )

    # The signature is not compatible with `object.__ne__()` on purpose.
    @overload  # type: ignore[override]
    def __ne__(
        self, other: ConstantValue, /
    ) -> Condition[IdentifierT, Literal["ne"], Constant, None]:
        ...

    @overload
    def __ne__(
        self, other: HasIdentifier[OtherIdentifierT], /
    ) -> Condition[IdentifierT, Literal["ne"], OtherIdentifierT, None]:
        ...

    @overload
    def __ne__(
        self,
        other: Union[
            ConstantValue,
            HasIdentifier[OtherIdentifierT],
            Operation[OtherIdentifierT],
        ],
        /,
    ) -> Condition[
        IdentifierT,
        Literal["ne"],
        Union[Constant, OtherIdentifierT, Operation[OtherIdentifierT]],
        None,
    ]:
        ...

    # The signature is not compatible with `object.__ne__()` on purpose.
    def __ne__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: Union[
            ConstantValue,
            HasIdentifier[OtherIdentifierT],
            Operation[OtherIdentifierT],
        ],
        /,
    ) -> Condition[
        IdentifierT,
        Literal["ne"],
        Union[Constant, OtherIdentifierT, Operation[OtherIdentifierT]],
        None,
    ]:
        assert other is not None, "Use `~isnull()` instead."
        return ComparisonCondition(
            subject=self._operation_operand,
            operator="ne",
            target=convert_to_operand(other),
        )
