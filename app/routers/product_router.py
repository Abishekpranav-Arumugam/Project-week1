from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.crud.product_crud import ProductCRUD
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)
from app.exceptions.custom_exceptions import ProductNotFoundError


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# ============================================================
# CREATE PRODUCT
# ============================================================

@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a product"
)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):

    crud = ProductCRUD(db)

    return crud.create_product(product_data)


# ============================================================
# GET ALL PRODUCTS
# ============================================================

@router.get(
    "/",
    response_model=list[ProductResponse],
    summary="Get all products"
)
def get_all_products(
    db: Session = Depends(get_db)
):

    crud = ProductCRUD(db)

    return crud.get_all_products()


# ============================================================
# GET PRODUCT BY ID
# ============================================================

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get product by ID"
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    crud = ProductCRUD(db)

    try:

        return crud.get_product_by_id(product_id)

    except ProductNotFoundError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )


# ============================================================
# UPDATE PRODUCT
# ============================================================

@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update a product"
)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):

    crud = ProductCRUD(db)

    try:

        return crud.update_product(
            product_id,
            product_data
        )

    except ProductNotFoundError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )


# ============================================================
# DELETE PRODUCT
# ============================================================

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product"
)

def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    crud = ProductCRUD(db)

    try:
        crud.delete_product(product_id)

        return None

    except ProductNotFoundError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )