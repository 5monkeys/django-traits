<h1 align=center>django-traits</h1>

Define traits for Django models that works seamlessly both in-Python and using the ORM,
with coordinated tests.

### Installation

```bash
$ python3 -m pip install django-traits
```

### Example

```python
class Rich(Trait["Person"]):
    def check_instance(self, instance: Person) -> bool:
        return instance.income > 1000

    def as_q(self) -> models.Q:
        return models.Q(income__gt=1000)


class Person(models.Model):
    is_rich = Rich()
    income = models.PositiveIntegerField()


# Filter for rich people, this uses the ORM predicate as defined in as_q().
rich_people = Person.is_rich.all()

# Check if a person is rich, this uses the in-Python predicate as defined in check_instance().
person = Person.objects.first()
if person.is_rich:
    print("Money is not a problem")
else:
    print("This person is not rich")
```

The automated test factory makes it simple to write tests that guarantess
that the in-Python and ORM predicates stay in sync.

```python
class TestPerson:
    test_is_rich = test_trait(
        (
            (PersonFactory(), False),
            (PersonFactory(income=1000), False),
            (PersonFactory(income=1001), True),
        )
    )
```

The above example will generate tests that exercises the in-Python predicate on instances of `Person`,
as well as tests that tries to filter using the ORM predicate.
