from typing import Callable
from typing import TypeVar

from traits import Trait

M = TypeVar("M")


def create_trait_test(trait: Trait[M]) -> Callable[[M], None]:
    model = trait._model
    attribute_name = next(
        name for name, value in model.__dict__.items() if value == trait
    )

    def test(instance: M) -> None:
        instance.save()
        assert isinstance(getattr(instance, attribute_name), bool)
        assert (
            getattr(instance, attribute_name)
            is model.objects.filter(trait.q, pk=instance.pk).exists()
        ), (
            f"Evaluated value of check_instance() did not match query result for "
            f"{type(trait).__qualname__!r}."
        )

    test.__name__ = f"test_trait_{attribute_name}"

    return test
