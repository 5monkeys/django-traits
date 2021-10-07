from __future__ import annotations

import abc
from typing import Generic
from typing import TypeVar
from typing import overload

from django.db import models

M = TypeVar("M", bound=models.Model)
S = TypeVar("S", bound="Trait")


class Trait(Generic[M], abc.ABC):
    def __init__(self) -> None:
        self._model: type[M] | None = None

    @property
    @abc.abstractmethod
    def q(self) -> models.Q:
        ...

    @abc.abstractmethod
    def check_instance(self, instance: M) -> bool:
        ...

    def all(self) -> models.QuerySet[M]:
        if self._model is None:
            raise TypeError(f"Can't call .all() on unbound {type(self).__qualname__}")
        return self._model.objects.filter(self.q)

    def __set_name__(self, owner: type[M], name: str) -> None:
        if self._model is not None:
            raise TypeError("Can't reuse bound trait")
        self._model = owner

    @overload
    def __get__(self: S, instance: None, owner: type[M]) -> S:
        ...

    @overload
    def __get__(self, instance: models.Model, owner: type[M]) -> bool:
        ...

    def __get__(self: S, instance: models.Model | None, owner: type[M]) -> bool | S:
        return self if instance is None else self.check_instance(instance)
