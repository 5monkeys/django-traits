from __future__ import annotations

from django.db import models

from traits import Trait


class Rich(Trait["Person"]):
    def check_instance(self, instance: Person) -> bool:
        return instance.income > 1000

    def as_q(self) -> models.Q:
        return models.Q(income__gt=1000)


class Person(models.Model):
    is_rich = Rich()
    income = models.PositiveIntegerField()
