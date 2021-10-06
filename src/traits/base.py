from __future__ import annotations

import abc
from typing import Generic
from typing import TypeVar

from django.db import models

# Would removing the bound here make it easier to make generic traits? Better to
# make sure the type of instance has the required fields for instance with
# protocols.
M = TypeVar("M", bound=models.Model)
S = TypeVar("S", bound="Trait")


class Trait(Generic[M], abc.ABC):
    _instance: M | None
    _owner: type[M]

    @abc.abstractmethod
    def as_q(self) -> models.Q:
        ...

    @abc.abstractmethod
    def check_instance(self, instance: M) -> bool:
        ...

    def __call__(self) -> bool:
        if self._instance is None:
            raise TypeError("Trait called without being bound to an instance")
        return self.check_instance(self._instance)

    def __bool__(self) -> bool:
        return self()

    # todo: Which hint works better? (The ModelTrait[M] one might be problematic
    #   when adding methods to a trait in subclasses).
    #   Need higher kinded type vars to type properly
    #   https://github.com/python/typing/issues/548
    #   The signature using "self: S" results in the return type of the all()
    #   method becoming QuerySet[Any], so apparently fails to bind M.
    # def __get__(self: S, instance: Optional[M], owner: Type[M]) -> S:
    def __get__(self: Trait[M], instance: M | None, owner: type[M]) -> Trait[M]:
        # TODO: Use inspect.isabstract() to make sure abstract traits can't be bound.
        # TODO: Assert instance is not None.
        self._instance = instance
        self._owner = owner
        return self

    def all(self) -> models.QuerySet[M]:
        return self._owner.objects.filter(self.as_q())
