from app.crud.product_crud import ProductCRUD
from app.database.connection import DatabaseManager
from app.exceptions.custom_exceptions import (
    DatabaseOperationError,
    ProductNotFoundError,
    ProductValidationError,
)
from app.models.product import Product
from app.utils.logger import logger


class ProductManagementApplication:
    """
    Main application class for Product Management System.
    """

    def __init__(self):
        self.database = DatabaseManager()
        self.product_crud = ProductCRUD(
            self.database
        )

    def start(self):
        """
        Start the application.
        """

        try:
            self.database.connect()

            logger.info(
                "Product Management Application started."
            )

            while True:
                self.display_menu()

                choice = input(
                    "Enter your choice: "
                ).strip()

                if choice == "1":
                    self.add_product()

                elif choice == "2":
                    self.view_products()

                elif choice == "3":
                    self.search_product()

                elif choice == "4":
                    self.update_product()

                elif choice == "5":
                    self.delete_product()

                elif choice == "6":
                    print(
                        "\nThank you for using "
                        "Product Management System."
                    )
                    break

                else:
                    print(
                        "\nInvalid choice. "
                        "Please select 1-6."
                    )

        except Exception as error:
            logger.exception(
                "Application encountered an unexpected error: %s",
                error,
            )

            print(
                "\nApplication error occurred."
            )

        finally:
            self.database.disconnect()

            logger.info(
                "Product Management Application stopped."
            )

    @staticmethod
    def display_menu():
        """
        Display the main menu.
        """

        print("\n")
        print("=" * 55)
        print("          PRODUCT MANAGEMENT SYSTEM")
        print("=" * 55)
        print("1. Add Product")
        print("2. View All Products")
        print("3. Search Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Exit")
        print("=" * 55)

    def add_product(self):
        """
        Create a new product.
        """

        print("\n--- ADD PRODUCT ---")

        try:
            name = input(
                "Product name: "
            ).strip()

            description = input(
                "Description: "
            ).strip()

            price = float(
                input("Price: ").strip()
            )

            quantity = int(
                input("Quantity: ").strip()
            )

            category = input(
                "Category: "
            ).strip()

            product = Product(
                name=name,
                description=description,
                price=price,
                quantity=quantity,
                category=category,
            )

            product_id = (
                self.product_crud.create_product(
                    product
                )
            )

            print(
                f"\nProduct created successfully!"
                f"\nProduct ID: {product_id}"
            )

        except ValueError as error:
            print(
                f"\nInvalid input: {error}"
            )

            logger.warning(
                "Invalid product input: %s",
                error,
            )

        except ProductValidationError as error:
            print(
                f"\nValidation error: {error}"
            )

        except DatabaseOperationError as error:
            print(
                f"\nDatabase error: {error}"
            )

    def view_products(self):
        """
        Display all products.
        """

        print("\n--- ALL PRODUCTS ---")

        try:
            products = (
                self.product_crud.get_all_products()
            )

            if not products:
                print(
                    "\nNo products found."
                )
                return

            print(
                "\n"
                f"{'ID':<5}"
                f"{'Name':<25}"
                f"{'Price':>12}"
                f"{'Quantity':>10}"
                f"  {'Category':<20}"
            )

            print("-" * 75)

            for product in products:
                print(
                    f"{product.id:<5}"
                    f"{product.name[:24]:<25}"
                    f"{product.price:>12.2f}"
                    f"{product.quantity:>10}"
                    f"  {product.category[:19]:<20}"
                )

        except DatabaseOperationError as error:
            print(
                f"\nDatabase error: {error}"
            )

    def search_product(self):
        """
        Search for a product using its ID.
        """

        print("\n--- SEARCH PRODUCT ---")

        try:
            product_id = int(
                input(
                    "Enter product ID: "
                ).strip()
            )

            product = (
                self.product_crud.get_product_by_id(
                    product_id
                )
            )

            print("\nProduct found:")
            print("-" * 40)
            print(f"ID          : {product.id}")
            print(f"Name        : {product.name}")
            print(
                f"Description : {product.description}"
            )
            print(
                f"Price       : {product.price:.2f}"
            )
            print(
                f"Quantity    : {product.quantity}"
            )
            print(
                f"Category    : {product.category}"
            )

        except ValueError:
            print(
                "\nProduct ID must be a number."
            )

        except ProductNotFoundError as error:
            print(
                f"\n{error}"
            )

        except ProductValidationError as error:
            print(
                f"\nValidation error: {error}"
            )

        except DatabaseOperationError as error:
            print(
                f"\nDatabase error: {error}"
            )

    def update_product(self):
        """
        Update an existing product.
        """

        print("\n--- UPDATE PRODUCT ---")

        try:
            product_id = int(
                input(
                    "Enter product ID: "
                ).strip()
            )

            existing = (
                self.product_crud.get_product_by_id(
                    product_id
                )
            )

            print(
                "\nCurrent product:"
            )

            print(
                f"Name       : {existing.name}"
            )
            print(
                f"Description: {existing.description}"
            )
            print(
                f"Price      : {existing.price:.2f}"
            )
            print(
                f"Quantity   : {existing.quantity}"
            )
            print(
                f"Category   : {existing.category}"
            )

            print(
                "\nEnter new values."
            )

            name = input(
                f"Name [{existing.name}]: "
            ).strip()

            description = input(
                f"Description "
                f"[{existing.description}]: "
            ).strip()

            price_input = input(
                f"Price [{existing.price}]: "
            ).strip()

            quantity_input = input(
                f"Quantity [{existing.quantity}]: "
            ).strip()

            category = input(
                f"Category [{existing.category}]: "
            ).strip()

            if not name:
                name = existing.name

            if not description:
                description = existing.description

            if not price_input:
                price = existing.price
            else:
                price = float(price_input)

            if not quantity_input:
                quantity = existing.quantity
            else:
                quantity = int(quantity_input)

            if not category:
                category = existing.category

            updated_product = Product(
                name=name,
                description=description,
                price=price,
                quantity=quantity,
                category=category,
            )

            self.product_crud.update_product(
                product_id,
                updated_product,
            )

            print(
                "\nProduct updated successfully."
            )

        except ValueError:
            print(
                "\nInvalid numeric value."
            )

        except ProductNotFoundError as error:
            print(
                f"\n{error}"
            )

        except ProductValidationError as error:
            print(
                f"\nValidation error: {error}"
            )

        except DatabaseOperationError as error:
            print(
                f"\nDatabase error: {error}"
            )

    def delete_product(self):
        """
        Delete a product.
        """

        print("\n--- DELETE PRODUCT ---")

        try:
            product_id = int(
                input(
                    "Enter product ID: "
                ).strip()
            )

            product = (
                self.product_crud.get_product_by_id(
                    product_id
                )
            )

            print(
                f"\nYou are about to delete:"
            )
            print(
                f"ID: {product.id}"
            )
            print(
                f"Name: {product.name}"
            )

            confirmation = input(
                "\nAre you sure? (y/n): "
            ).strip().lower()

            if confirmation != "y":
                print(
                    "\nDelete operation cancelled."
                )
                return

            self.product_crud.delete_product(
                product_id
            )

            print(
                "\nProduct deleted successfully."
            )

        except ValueError:
            print(
                "\nProduct ID must be a number."
            )

        except ProductNotFoundError as error:
            print(
                f"\n{error}"
            )

        except ProductValidationError as error:
            print(
                f"\nValidation error: {error}"
            )

        except DatabaseOperationError as error:
            print(
                f"\nDatabase error: {error}"
            )


def main():
    """
    Application entry point.
    """

    application = (
        ProductManagementApplication()
    )

    application.start()


if __name__ == "__main__":
    main()