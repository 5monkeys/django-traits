from __future__ import annotations

from django.db import models

from traits import Trait


class Rich(Trait["Person"]):
    q = models.Q(income__gt=1000)

    def check_instance(self, instance: Person) -> bool:
        return instance.income > 1000


class Person(models.Model):
    is_rich = Rich()
    income = models.PositiveIntegerField()


class ComplexTrait(Trait["ComplexModel"]):
    q = models.Q(a__gte=0, b__lt=0, c__gte=0) | models.Q(a__lt=0, b__gte=0, c__lt=0)

    def check_instance(self, instance: ComplexModel) -> bool:
        return (instance.a >= 0 and instance.b < 0 and instance.c >= 0) or (
            instance.a < 0 and instance.b >= 0 and instance.c < 0
        )


class ComplexModel(models.Model):
    a = models.IntegerField()
    b = models.IntegerField()
    c = models.IntegerField()
    is_complex = ComplexTrait()


class BrokenTrait(Trait["BrokenModel"]):
    q = models.Q(a__gt=0, b__lt=0)

    def check_instance(self, instance: BrokenModel) -> bool:
        return instance.a < 0 and instance.b > 0


class BrokenModel(models.Model):
    foo = BrokenTrait()
    a = models.IntegerField()
    b = models.IntegerField()
