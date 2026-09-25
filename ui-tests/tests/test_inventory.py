import pytest

pytestmark = pytest.mark.regression


@pytest.mark.parametrize(
    "sort_value,attribute,reverse",
    [
        pytest.param("az", "names", False, id="name-ascending"),
        pytest.param("za", "names", True, id="name-descending"),
        pytest.param("lohi", "prices", False, id="price-ascending"),
        pytest.param("hilo", "prices", True, id="price-descending"),
    ],
)
def test_product_sorting(inventory, sort_value, attribute, reverse):
    original = getattr(inventory, attribute)
    assert len(original) == 6
    inventory.sort(sort_value)
    actual = getattr(inventory, attribute)
    assert actual == sorted(original, reverse=reverse)
