from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.crud.sale_crud import SaleCRUD

from app.database.connection import get_db

from app.exceptions.custom_exceptions import (
    ProductNotFoundError,
    InsufficientStockError,
    InvalidSaleQuantityError,
)

from app.schemas.sale import (
    SaleCreate,
    SaleResponse,
)


router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
)


# ==========================================================
# CREATE SALE / BUY PRODUCT
# ==========================================================

@router.post(
    "/",
    response_model=SaleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Purchase a product and reduce inventory",
)
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db),
):

    try:

        return SaleCRUD.create_sale(
            db,
            sale
        )

    except ProductNotFoundError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )

    except InsufficientStockError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    except InvalidSaleQuantityError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


# ==========================================================
# GET ALL SALES
# ==========================================================

@router.get(
    "/",
    response_model=list[SaleResponse],
    summary="Get all sales",
)
def get_sales(
    db: Session = Depends(get_db),
):

    return SaleCRUD.get_all(db)


# ==========================================================
# GET SALE BY ID
# ==========================================================

@router.get(
    "/{sale_id}",
    response_model=SaleResponse,
    summary="Get sale by ID",
)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
):

    sale = SaleCRUD.get_by_id(
        db,
        sale_id
    )

    if sale is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sale with ID {sale_id} not found.",
        )

    return sale