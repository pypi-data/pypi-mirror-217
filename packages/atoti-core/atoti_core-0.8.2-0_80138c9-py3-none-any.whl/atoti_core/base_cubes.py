from collections.abc import Mapping
from typing import TypeVar

from .base_cube import BaseCubeBound
from .repr_json import ReprJson, ReprJsonable

CubeT = TypeVar("CubeT", bound=BaseCubeBound, covariant=True)


class BaseCubes(Mapping[str, CubeT], ReprJsonable):
    def _repr_json_(self) -> ReprJson:
        """Return the JSON representation of cubes."""
        return (
            {name: cube._repr_json_()[0] for name, cube in sorted(self.items())},
            {"expanded": False, "root": "Cubes"},
        )


BaseCubesBound = BaseCubes[BaseCubeBound]
