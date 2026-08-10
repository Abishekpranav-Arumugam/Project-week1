class ProductNotFoundError(Exception):
    """
    Raised when a requested product does not exist.
    """

    def __init__(self, product_id):
        self.product_id = product_id

        super().__init__(
            f"Product with ID {product_id} was not found."
        )


class ProductValidationError(Exception):
    """
    Raised when product data is invalid.
    """

    pass


class DatabaseOperationError(Exception):
    """
    Raised when a database operation fails.
    """

    pass