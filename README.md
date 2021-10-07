<p align=center><img src=docs/logo.svg width=200/></p>


<h1 align=center>django-traits</h1>

<p align=center>
    <a href=https://github.com/5monkeys/django-traits/actions?query=workflow%3ACI+branch%3Amain><img src=https://github.com/5monkeys/django-traits/workflows/CI/badge.svg alt="CI Build Status"></a>
    <a href=https://codecov.io/gh/5monkeys/django-traits><img src="https://codecov.io/gh/5monkeys/django-traits/branch/main/graph/badge.svg?token=U6BK5DWAWD" alt="Test coverage reports"/></a>
</p>

Define traits for Django models that works seamlessly both in-Python and using the ORM,
with coordinated tests.

### Installation

```bash
$ python3 -m pip install django-traits
```

### Example

```python
class Rich(Trait["Person"]):
    q = models.Q(income__gt=1000)

    def check_instance(self, instance: Person) -> bool:
        return instance.income > 1000


class Person(models.Model):
    is_rich = Rich()
    income = models.PositiveIntegerField()


# Filter for rich people, this uses the ORM predicate as defined in q.
rich_people = Person.is_rich.all()

# Check if a person is rich, this uses the in-Python predicate as defined in check_instance().
person = Person.objects.first()
if person.is_rich:
    print("Money is not a problem")
else:
    print("This person is not rich")
```

The automated test factory makes it simple to write tests that guarantees that the
in-Python predicate stays in sync with its ORM counterpart. The following example
generates parameterized tests that checks boundary values.



```python
import pytest
from traits.tests import create_trait_test


parametrize_people = pytest.mark.parametrize(
    "instance",
    PersonFactory(),
    PersonFactory(income=1000),
    PersonFactory(income=1001),
)


class TestPerson:
    test_is_rich = parametrize_people(create_trait_test(Person.is_rich))
```

The above example will generate three tests that checks that each given instance of
`Person` only appears in an ORM query result if the trait evaluates to `True` for that
instance, and that the result set is empty if it evaluates to `False`. So if the
implementations were to drift apart, for instance if the limit was increased to `2000`
in `check_instance()` but not in `q`, the tests would fail and enforce that the two
implementations are in sync.

You can also use [Hypothesis] to automatically generate test values.

```python
from traits.tests import create_trait_test
from hypothesis import given
from hypothesis.strategies import builds
from hypothesis.strategies import integers

people = builds(
    PersonFactory.build,
    income=integers(-9223372036854775808, 9223372036854775807),
)


class TestPerson:
    test_is_rich = given(people)(create_trait_test(Person.is_rich))
```


[Hypothesis]: https://github.com/HypothesisWorks/hypothesis
