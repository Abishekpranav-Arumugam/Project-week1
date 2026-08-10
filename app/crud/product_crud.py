from mysql.connector import Error

from app.database.connection import DatabaseManager
from app.exceptions.custom_exceptions import (
    ProductNotFoundError,
    ProductValidationError,
    DatabaseOperationError,
)
from app.models.product import Product
from app.utils.logger import logger


class ProductCRUD:
    """
    Handles all CRUD operations for products.
    """

    def __init__(self, database_manager=None):
        self.db = database_manager or DatabaseManager()

    # =========================================================
    # CREATE
    # =========================================================

    def create_product(self, product):
        """
        Insert a new product into the database.

        Returns:
            int: ID of the newly created product.
        """

        try:
            if not isinstance(product, Product):
                raise ProductValidationError(
                    "Expected a Product object."
                )

            product.validate()

            query = """
                INSERT INTO products
                (
                    name,
                    description,
                    price,
                    quantity,
                    category
                )
                VALUES (%s, %s, %s, %s, %s)
            """

            parameters = (
                product.name.strip(),
                product.description,
                product.price,
                product.quantity,
                product.category.strip(),
            )

            connection = self.db.get_connection()

            cursor = connection.cursor()

            cursor.execute(
                query,
                parameters,
            )

            connection.commit()

            product_id = cursor.lastrowid

            cursor.close()

            logger.info(
                "Product created successfully. ID=%s",
                product_id,
            )

            return product_id

        except ValueError as error:
            logger.warning(
                "Product validation failed: %s",
                error,
            )

            raise ProductValidationError(
                str(error)
            ) from error

        except Error as error:
            logger.error(
                "Failed to create product: %s",
                error,
            )

            if self.db.connection:
                self.db.connection.rollback()

            raise DatabaseOperationError(
                "Unable to create product."
            ) from error

        except Exception as error:
            logger.exception(
                "Unexpected error while creating product."
            )

            if self.db.connection:
                self.db.connection.rollback()

            raise DatabaseOperationError(
                "Unexpected error while creating product."
            ) from error

    # =========================================================
    # READ ALL
    # =========================================================

    def get_all_products(self):
        """
        Retrieve all products.
        """

        query = """
            SELECT
                id,
                name,
                description,
                price,
                quantity,
                category,
                created_at,
                updated_at
            FROM products
            ORDER BY id
        """

        try:
            rows = self.db.fetch_all(query)

            products = []

            for row in rows:
                product = Product(
                    id=row["id"],
                    name=row["name"],
                    description=row["description"],
                    price=float(row["price"]),
                    quantity=row["quantity"],
                    category=row["category"],
                )

                products.append(product)

            logger.info(
                "Retrieved %s products.",
                len(products),
            )

            return products

        except Error as error:
            logger.error(
                "Failed to retrieve products: %s",
                error,
            )

            raise DatabaseOperationError(
                "Unable to retrieve products."
            ) from error

    # =========================================================
    # READ ONE
    # =========================================================

    def get_product_by_id(self, product_id):
        """
        Retrieve a product using its ID.
        """

        if not isinstance(product_id, int):
            raise ProductValidationError(
                "Product ID must be an integer."
            )

        if product_id <= 0:
            raise ProductValidationError(
                "Product ID must be greater than zero."
            )

        query = """
            SELECT
                id,
                name,
                description,
                price,
                quantity,
                category,
                created_at,
                updated_at
            FROM products
            WHERE id = %s
        """

        try:
            row = self.db.fetch_one(
                query,
                (product_id,),
            )

            if row is None:
                logger.warning(
                    "Product ID=%s was not found.",
                    product_id,
                )

                raise ProductNotFoundError(product_id)

            product = Product(
                id=row["id"],
                name=row["name"],
                description=row["description"],
                price=float(row["price"]),
                quantity=row["quantity"],
                category=row["category"],
            )

            return product

        except ProductNotFoundError:
            raise

        except Error as error:
            logger.error(
                "Failed to retrieve product ID=%s: %s",
                product_id,
                error,
            )

            raise DatabaseOperationError(
                "Unable to retrieve product."
            ) from error

    # =========================================================
    # UPDATE
    # =========================================================

    def update_product(self, product_id, product):
        """
        Update an existing product.
        """

        if not isinstance(product_id, int):
            raise ProductValidationError(
                "Product ID must be an integer."
            )

        if product_id <= 0:
            raise ProductValidationError(
                "Product ID must be greater than zero."
            )

        if not isinstance(product, Product):
            raise ProductValidationError(
                "Expected a Product object."
            )

        try:
            product.validate()

            existing_product = self.get_product_by_id(
                product_id
            )

            if existing_product is None:
                raise ProductNotFoundError(product_id)

            query = """
                UPDATE products
                SET
                    name = %s,
                    description = %s,
                    price = %s,
                    quantity = %s,
                    category = %s
                WHERE id = %s
            """

            parameters = (
                product.name.strip(),
                product.description,
                product.price,
                product.quantity,
                product.category.strip(),
                product_id,
            )

            affected_rows = self.db.execute_query(
                query,
                parameters,
            )

            if affected_rows == 0:
                raise ProductNotFoundError(product_id)

            logger.info(
                "Product ID=%s updated successfully.",
                product_id,
            )

            return True

        except ProductNotFoundError:
            raise

        except ValueError as error:
            logger.warning(
                "Product validation failed: %s",
                error,
            )

            raise ProductValidationError(
                str(error)
            ) from error

        except Error as error:
            logger.error(
                "Failed to update product ID=%s: %s",
                product_id,
                error,
            )

            raise DatabaseOperationError(
                "Unable to update product."
            ) from error

    # =========================================================
    # DELETE
    # =========================================================

    def delete_product(self, product_id):
        """
        Delete a product using its ID.
        """

        if not isinstance(product_id, int):
            raise ProductValidationError(
                "Product ID must be an integer."
            )

        if product_id <= 0:
            raise ProductValidationError(
                "Product ID must be greater than zero."
            )

        try:
            existing_product = self.get_product_by_id(
                product_id
            )

            if existing_product is None:
                raise ProductNotFoundError(product_id)

            query = """
                DELETE FROM products
                WHERE id = %s
            """

            affected_rows = self.db.execute_query(
                query,
                (product_id,),
            )

            if affected_rows == 0:
                raise ProductNotFoundError(product_id)

            logger.info(
                "Product ID=%s deleted successfully.",
                product_id,
            )

            return True

        except ProductNotFoundError:
            raise

        except Error as error:
            logger.error(
                "Failed to delete product ID=%s: %s",
                product_id,
                error,
            )

            raise DatabaseOperationError(
                "Unable to delete product."
            ) from error