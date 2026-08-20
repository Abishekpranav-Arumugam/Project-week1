from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import (
    ProductNotFoundError,
    InsufficientStockError,
    InvalidSaleQuantityError,
)

from app.models.product import Product
from app.models.sale import Sale
from app.schemas.sale import SaleCreate


class SaleCRUD:

    @staticmethod
    def create_sale(
        db: Session,
        sale_data: SaleCreate,
    ) -> Sale:

        if sale_data.quantity <= 0:
            raise InvalidSaleQuantityError(
                "Sale quantity must be greater than zero."
            )

        try:

            # Lock the product row.
            statement = (
                select(Product)
                .where(
                    Product.id == sale_data.product_id
                )
                .with_for_update()
            )

            product = db.execute(
                statement
            ).scalar_one_or_none()

            # Product does not exist
            if product is None:
                raise ProductNotFoundError(
                    f"Product with ID "
                    f"{sale_data.product_id} not found."
                )

            # Check available stock
            if product.quantity < sale_data.quantity:
                raise InsufficientStockError(
                    f"Insufficient stock for "
                    f"'{product.name}'. "
                    f"Available: {product.quantity}, "
                    f"Requested: {sale_data.quantity}."
                )

            # Calculate total
            total_amount = (
                Decimal(str(product.price))
                * sale_data.quantity
            )

            # Reduce inventory
            product.quantity -= sale_data.quantity

            # Create sale
            sale = Sale(
                product_id=product.id,
                quantity=sale_data.quantity,
                total_amount=float(total_amount),

                # Explicitly set timestamp
                created_at=datetime.utcnow(),
            )

            db.add(sale)

            # Save product quantity + sale together
            db.commit()

            # Get generated ID and timestamp
            db.refresh(sale)

            return sale

        except (
            ProductNotFoundError,
            InsufficientStockError,
            InvalidSaleQuantityError,
        ):
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(
        db: Session,
    ) -> list[Sale]:

        statement = select(Sale)

        result = db.execute(statement)

        return list(result.scalars().all())

    @staticmethod
    def get_by_id(
        db: Session,
        sale_id: int,
    ) -> Sale | None:

        return db.get(Sale, sale_id)