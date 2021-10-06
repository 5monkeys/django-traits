<h1 align=center>django-traits</h1>

Define traits for Django models that works seamlessly both in-Python and using the ORM,
with coordinated tests.

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
