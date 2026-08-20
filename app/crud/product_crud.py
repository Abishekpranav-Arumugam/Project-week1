from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.exceptions.custom_exceptions import ProductNotFoundError


class ProductCRUD:
    """
    Handles all database operations related to products.

    CRUD:

    C - Create
    R - Read
    U - Update
    D - Delete
    """

    def __init__(self, db: Session):
        self.db = db

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------

    def create_product(self, product_data: ProductCreate) -> Product:

        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            quantity=product_data.quantity,
            category=product_data.category
        )

        try:
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)

            return product

        except Exception:
            self.db.rollback()
            raise

    # ---------------------------------------------------------
    # READ - ALL PRODUCTS
    # ---------------------------------------------------------

    def get_all_products(self) -> list[Product]:

        return (
            self.db.query(Product)
            .order_by(Product.id)
            .all()
        )

    # ---------------------------------------------------------
    # READ - PRODUCT BY ID
    # ---------------------------------------------------------

    def get_product_by_id(self, product_id: int) -> Product:

        product = (
            self.db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        if product is None:
            raise ProductNotFoundError(
                f"Product with ID {product_id} not found"
            )

        return product

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    def update_product(
        self,
        product_id: int,
        product_data: ProductUpdate
    ) -> Product:

        product = self.get_product_by_id(product_id)

        update_data = product_data.model_dump(
            exclude_unset=True
        )

        try:

            for field, value in update_data.items():
                setattr(product, field, value)

            self.db.commit()
            self.db.refresh(product)

            return product

        except Exception:
            self.db.rollback()
            raise

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    def delete_product(self, product_id: int) -> Product:

        product = self.get_product_by_id(product_id)

        try:

            self.db.delete(product)
            self.db.commit()

            return product

        except Exception:
            self.db.rollback()
            raise