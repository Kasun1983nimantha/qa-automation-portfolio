from decimal import Decimal

import pytest

pytestmark = pytest.mark.regression


@pytest.mark.smoke
def test_cart_preserves_selected_products(inventory):
    inventory.add("sauce-labs-backpack").add("sauce-labs-bike-light")
    assert inventory.cart_count == 2
    cart = inventory.open_cart()
    assert cart.items == [
        {"name": "Sauce Labs Backpack", "price": Decimal("29.99"), "quantity": 1},
        {"name": "Sauce Labs Bike Light", "price": Decimal("9.99"), "quantity": 1},
    ]
    cart.remove("sauce-labs-backpack")
    assert cart.cart_count == 1
    assert cart.items == [
        {"name": "Sauce Labs Bike Light", "price": Decimal("9.99"), "quantity": 1},
    ]


def test_remove_last_product_clears_cart(inventory):
    inventory.add("sauce-labs-backpack").remove("sauce-labs-backpack")
    assert inventory.cart_count == 0
    assert inventory.open_cart().items == []


def test_cart_survives_refresh(inventory):
    inventory.add("sauce-labs-bike-light")
    cart = inventory.open_cart()
    before = cart.items
    assert len(before) == 1
    cart.driver.refresh()
    assert cart.items == before
    assert cart.cart_count == 1
