from __future__ import annotations

import abc
from functools import cached_property
from typing import Generic
from typing import TypeVar
from typing import final
from typing import overload

from django.db import models

M = TypeVar("M", bound=models.Model)


class Trait(Generic[M], abc.ABC):
    def __init__(self) -> None:
        self._model: type[M] | None = None

    @abc.abstractmethod
    def as_q(self) -> models.Q:
        ...

    @abc.abstractmethod
    def check_instance(self, instance: M) -> bool:
        ...

    @final
    @cached_property
    def q(self) -> models.Q:
        return self.as_q()

    def all(self) -> models.QuerySet[M]:
        # TODO: Good error message.
        assert self._model is not None
        return self._model.objects.filter(self.as_q())

    @overload
    def __get__(self: Trait[M], instance: M, owner: type[M]) -> bool:
        ...

    @overload
    def __get__(self: Trait[M], instance: None, owner: type[M]) -> Trait[M]:
        ...

    def __get__(self: Trait[M], instance: M | None, owner: type[M]) -> bool | Trait[M]:
        # TODO: Use inspect.isabstract() to make sure abstract traits can't be bound.
        if self._model is None:
            self._model = owner
        else:
            assert self._model is owner
        if instance is None:
            return self
        else:
            return self.check_instance(instance)
