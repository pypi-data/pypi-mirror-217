# SPDX-License-Identifier: MIT
"""Argument polymorphism utility."""

from collections.abc import Iterator, KeysView, Mapping
from typing import Generic, Self, TypeVar

T = TypeVar('T')

class Registry(Generic[T]):
    """
    Used to enable argument polymorphism.

    Several operations have arguments that can take any of three forms:
    - a value of a type T;
    - a string, looked up to get a value of type T;
    - None, indicating a default value.
    """

    def __init__(self, name: str | None = None) -> None:
        self.dict: dict[str, T] = {}
        self.default: T | None = None
        self.name = name

    def __copy__(self) -> Self:
        r = type(self)(self.name)
        r.dict = self.dict.copy()
        r.default = self.default
        return r

    def __iter__(self) -> Iterator[str]:
        return iter(self.dict)

    def update(self, m: Mapping[str, T]) -> Self:
        self.dict.update(m)
        return self

    def set_default(self, e: T | str | None) -> Self:
        self.default = self.get(e)
        return self

    def get(self, t: T | str | None = None) -> T:
        if t is None:
            if self.default is None:
                msg = 'no default value'
                raise self._keyerror(msg)
            return self.default
        if isinstance(t, str):
            try:
                return self.dict[t]
            except KeyError as e:
                msg = f'‘{t}’ is not known'
                raise self._keyerror(msg) from e
        return t

    def keys(self) -> KeysView[str]:
        return self.dict.keys()

    def _keyerror(self, message: str) -> KeyError:
        if self.name:
            message = self.name + ': ' + message
        return KeyError(message)
