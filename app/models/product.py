from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    """
    Represents a product in the application.
    """

    name: str
    description: Optional[str]
    price: float
    quantity: int
    category: str
    id: Optional[int] = None

    def validate(self):
        """
        Validate product data before sending it to MySQL.
        """

        if not self.name or not self.name.strip():
            raise ValueError("Product name cannot be empty.")

        if len(self.name.strip()) > 100:
            raise ValueError(
                "Product name cannot exceed 100 characters."
            )

        if self.description and len(self.description) > 500:
            raise ValueError(
                "Description cannot exceed 500 characters."
            )

        if self.price < 0:
            raise ValueError(
                "Product price cannot be negative."
            )

        if self.quantity < 0:
            raise ValueError(
                "Product quantity cannot be negative."
            )

        if not self.category or not self.category.strip():
            raise ValueError(
                "Product category cannot be empty."
            )

        if len(self.category.strip()) > 100:
            raise ValueError(
                "Category cannot exceed 100 characters."
            )

    def __str__(self):
        return (
            f"Product("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"price={self.price:.2f}, "
            f"quantity={self.quantity}, "
            f"category='{self.category}'"
            f")"
        )