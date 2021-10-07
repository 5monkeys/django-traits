import pytest
from django.db import models

from traits import Trait

from .app.models import Person


@pytest.mark.django_db
def test_basics() -> None:
    rich = Person.objects.create(income=2000)
    poor = Person.objects.create(income=500)
    query_rich = Person.is_rich.all()
    assert list(query_rich) == [rich]
    query_poor = Person.objects.filter(~Person.is_rich.q)
    assert list(query_poor) == [poor]


def test_instantiating_abstract_traits_raises_type_error() -> None:
    class MissingCheckInstance(Trait):
        q = models.Q()

    class MissingQ(Trait):
        def check_instance(self, instance: models.Model) -> bool:
            return True

    raises = pytest.raises(TypeError, match=r"^Can't instantiate")

    with raises:
        MissingCheckInstance()  # type: ignore[abstract]
    with raises:
        MissingQ()  # type: ignore[abstract]


class DummyTrait(Trait):
    q = models.Q()

    def check_instance(self, instance: models.Model) -> bool:
        return True


def test_reusing_bound_trait_raises_type_error() -> None:
    class ConflictingOwner:
        trait = DummyTrait()

    with pytest.raises(RuntimeError) as exc_info:

        class _:
            trait = ConflictingOwner.trait

    assert type(exc_info.value.__cause__) is TypeError
    assert str(exc_info.value.__cause__) == "Can't reuse bound trait"


def test_filtering_unbound_trait_raises_type_error() -> None:
    unbound = DummyTrait()
    with pytest.raises(
        TypeError,
        match=fr"Can't call \.all\(\) on unbound {DummyTrait.__qualname__}",
    ):
        unbound.all()
