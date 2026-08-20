# Python Utility Project : Foundation & Workspace Setup

## Overview
This project provides Python utilities utilizing standard Linux commands and environment configurations.

## Prerequisites
To run and develop within this project, your system must meet the following requirements:

### Operating System Requirements
* Developed and tested on **Linux** (e.g., Ubuntu/Debian, CentOS/RHEL).
* Requires standard Linux command-line utilities.

### Network Requirements
* Outbound internet access required for downloading Python dependencies via pip.
* DNS resolution configured correctly.

### Software Requirements
* Python 3.8+
* Git

## Environment Setup
1. Create a VIRTUAL ENVIRONMENT => python3 -m venv venv
2. Activate the VIRTUAL ENVIRONMENT => source venv/bin/activate

## App folder (backend) — What I implemented

I implemented the backend application inside the app/ folder. Key items:

- [app/main.py](app/main.py): (FastAPI/Flask setup and startup).
- [app/config/settings.py](app/config/settings.py):
- [app/crud/product_crud.py](app/crud/product_crud.py) 
- [app/crud/sale_crud.py](app/crud/sale_crud.py):
- [app/database/connection.py](app/database/connection.py): 
- [app/exceptions/custom_exceptions.py](app/exceptions/custom_exceptions.py):
- [app/models/product.py](app/models/product.py) 
- [app/models/sale.py](app/models/sale.py):
- [app/routers/product_router.py](app/routers/product_router.py)
- [app/routers/sale_router.py](app/routers/sale_router.py):
- [app/schemas/product.py](app/schemas/product.py) and [app/schemas/sale.py](app/schemas/sale.py)
- [app/utils/logger.py](app/utils/logger.py)

This README section intentionally focuses only on work done inside the app/ folder; frontend and other project areas are omitted.

## CRUD operations (app/crud)

Summary of implemented CRUD functionality and important behaviors:

- Product CRUD ([app/crud/product_crud.py](app/crud/product_crud.py)):
	- `create_product(product_data: ProductCreate) -> Product`: creates a new `Product` record from the provided schema and returns the created instance.
	- `get_all_products() -> list[Product]`: returns all products ordered by `id`.
	- `get_product_by_id(product_id: int) -> Product`: fetches a single product by id; raises `ProductNotFoundError` if not found.
	- `update_product(product_id: int, product_data: ProductUpdate) -> Product`: applies partial updates (excludes unset fields), commits, and returns the updated product.
	- `delete_product(product_id: int) -> Product`: deletes the product and returns the deleted instance.
	- Transactions: commits on success and rolls back on exceptions.

- Sale CRUD ([app/crud/sale_crud.py](app/crud/sale_crud.py)):
	- `create_sale(db: Session, sale_data: SaleCreate) -> Sale`: validates `quantity > 0`, locks the related `Product` row using `SELECT ... FOR UPDATE`, checks stock, decrements product quantity, creates a `Sale` record (sets `created_at`), commits both changes together, and returns the sale. Raises `InvalidSaleQuantityError`, `ProductNotFoundError`, or `InsufficientStockError` on validation/failure.
	- `get_all(db: Session) -> list[Sale]`: returns all sales.
	- `get_by_id(db: Session, sale_id: int) -> Sale | None`: returns a sale by id or `None`.

These implementations use the schemas in [app/schemas](app/schemas) and models in [app/models](app/models), and error classes in [app/exceptions/custom_exceptions.py](app/exceptions/custom_exceptions.py).

## Git workflow (basics)

Typical basic git commands used in this project:

# create a branch and switch to it
git checkout -b branch4

# stage and commit changes
git add .
git commit -m "Describe changes"

# push the branch to origin
git push origin branch4

git checkout main
git pull origin main

git merge branch4
git push origin main
```
