import pytest

from .app.models import Person


@pytest.mark.django_db
def test_basics() -> None:
    rich = Person.objects.create(income=2000)
    poor = Person.objects.create(income=500)
    query_rich = Person.is_rich.all()
    assert list(query_rich) == [rich]
    query_poor = Person.objects.filter(~Person.is_rich.as_q())
    assert list(query_poor) == [poor]
