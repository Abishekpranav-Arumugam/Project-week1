import pytest

from app.models.product import Product


def test_product_creation():
    product = Product(
        name="Laptop",
        description="Test laptop",
        price=50000.00,
        quantity=10,
        category="Electronics",
    )

    assert product.name == "Laptop"
    assert product.price == 50000.00
    assert product.quantity == 10
    assert product.category == "Electronics"


def test_product_validation_success():
    product = Product(
        name="Mouse",
        description="Wireless mouse",
        price=1000.00,
        quantity=5,
        category="Accessories",
    )

    product.validate()


def test_product_empty_name():
    product = Product(
        name="",
        description="Test",
        price=100.00,
        quantity=1,
        category="Test",
    )

    with pytest.raises(ValueError):
        product.validate()


def test_product_negative_price():
    product = Product(
        name="Laptop",
        description="Test",
        price=-100.00,
        quantity=1,
        category="Electronics",
    )

    with pytest.raises(ValueError):
        product.validate()


def test_product_negative_quantity():
    product = Product(
        name="Laptop",
        description="Test",
        price=100.00,
        quantity=-1,
        category="Electronics",
    )

    with pytest.raises(ValueError):
        product.validate()