from decimal import Decimal

import pytest

pytestmark = pytest.mark.regression


@pytest.fixture
def checkout(inventory):
    return inventory.add("sauce-labs-backpack").add("sauce-labs-bike-light").open_cart().checkout()


@pytest.mark.smoke
def test_complete_purchase(checkout):
    checkout.submit_customer("Alex", "Tester", "5000")
    assert checkout.title == "Checkout: Overview"
    assert checkout.items == [
        {"name": "Sauce Labs Backpack", "price": Decimal("29.99"), "quantity": 1},
        {"name": "Sauce Labs Bike Light", "price": Decimal("9.99"), "quantity": 1},
    ]
    assert checkout.subtotal == Decimal("39.98")
    # Demo app's observed tax rule is 8%, rounded to cents; not a real tax calculation.
    assert checkout.tax == Decimal("3.20")
    assert checkout.total == Decimal("43.18")
    assert checkout.total == checkout.subtotal + checkout.tax
    assert checkout.finish() == "Thank you for your order!"
    assert checkout.cart_count == 0
    assert checkout.open_cart().items == []


@pytest.mark.parametrize(
    "first,last,postal,error",
    [
        pytest.param("", "Tester", "5000", "First Name is required", id="missing-first-name"),
        pytest.param("Alex", "", "5000", "Last Name is required", id="missing-last-name"),
        pytest.param("Alex", "Tester", "", "Postal Code is required", id="missing-postal-code"),
    ],
)
def test_customer_fields_are_required(checkout, first, last, postal, error):
    checkout.submit_customer(first, last, postal)
    assert error in checkout.error
    assert checkout.title == "Checkout: Your Information"
    assert checkout.cart_count == 2


def test_cancel_overview_preserves_cart(checkout):
    checkout.submit_customer("Alex", "Tester", "5000")
    assert checkout.title == "Checkout: Overview"
    inventory = checkout.cancel_overview()
    assert inventory.title == "Products"
    assert inventory.cart_count == 2
    assert len(inventory.open_cart().items) == 2
