from dataclasses import dataclass

from typing_extensions import Self

from .identifier import Identifier


@dataclass(frozen=True)
class HierarchyIdentifier(Identifier):  # pylint: disable=keyword-only-dataclass
    dimension_name: str
    hierarchy_name: str

    @classmethod
    def from_java_description(cls, java_description: str, /) -> Self:
        hierarchy_name, dimension_name = java_description.split("@")
        return cls(dimension_name, hierarchy_name)

    @property
    def key(self) -> tuple[str, str]:
        return self.dimension_name, self.hierarchy_name

    def __repr__(self) -> str:
        return f"h[{self.key}]"
