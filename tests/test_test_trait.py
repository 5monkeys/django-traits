import pytest
from hypothesis import given
from hypothesis.strategies import builds
from hypothesis.strategies import integers

from traits.tests import create_trait_test

from .app.models import BrokenModel
from .app.models import ComplexModel

sql_integers = integers(min_value=-(2 ** 63), max_value=2 ** 63 - 1)

generate_complex = builds(ComplexModel, a=sql_integers, b=sql_integers, c=sql_integers)
test_generated_tests_for_complex_passes = given(generate_complex)(
    pytest.mark.django_db(transaction=True)(create_trait_test(ComplexModel.is_complex))
)

generate_broken = builds(BrokenModel, a=sql_integers, b=sql_integers)
test_generated_tests_for_broken_passes = pytest.mark.xfail(strict=True)(
    given(generate_broken)(
        pytest.mark.django_db(transaction=True)(create_trait_test(BrokenModel.foo))
    )
)
