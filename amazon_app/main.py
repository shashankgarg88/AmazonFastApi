import io
from typing import List

import uvicorn
from fastapi import Depends, FastAPI, UploadFile
from sqlalchemy.orm import Session
import pandas as pd
from starlette.responses import StreamingResponse

from . import models, schemas
from .constants import column_mapping, numeric_colums
from .crud import get_product_markup, create_products, create_static_cost_factor, transform_excel_data, \
    bulk_update_products, create_product_objects
from .database import SessionLocal, engine, SQLALCHEMY_DATABASE_URL
from .sql_wrapper import ProductsDBMapper

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/products/", response_model=List[schemas.Product])
async def upload_products(file: UploadFile, db: Session = Depends(get_db)):
    print("file recievd")

    f = await file.read()
    excel_file = io.BytesIO(f)
    product_data = pd.read_excel(excel_file,
                                 sheet_name=None, engine='openpyxl')
    df = product_data['Sheet1']
    df = transform_excel_data(df)
    df['is_active'] = True
    products = create_products(db, df)
    print("data inserted")
    return products


@app.post("/update_products/", response_model=List[schemas.Product])
async def update_products(file: UploadFile):
    print("file recievd")

    f = await file.read()
    excel_file = io.BytesIO(f)
    product_data = pd.read_excel(excel_file,
                                 sheet_name=None, engine='openpyxl')
    df = product_data['Sheet1']
    df = transform_excel_data(df)
    df['is_active'] = True
    products = bulk_update_products(df)
    product_list = create_product_objects(products)
    print("data updated")
    return product_list


@app.post("/delete_products/", response_model=List[schemas.Product])
async def delete_products(file: UploadFile):
    print("file recievd")

    f = await file.read()
    excel_file = io.BytesIO(f)
    product_data = pd.read_excel(excel_file,
                                 sheet_name=None, engine='openpyxl')
    df = product_data['Sheet1']
    df = transform_excel_data(df)
    products = bulk_update_products(df)
    product_list = create_product_objects(products)
    print("data updated")
    return product_list


@app.get("/products/download", response_model=List[schemas.Product])
def download_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    df = pd.read_sql("select * from product;", engine)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        df.to_excel(writer, index=False)
    return StreamingResponse(
        io.BytesIO(buffer.getvalue()),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": f"attachment; filename=products.xlsx"}
    )


@app.get("/all_products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    df = pd.read_sql("select * from product", engine)
    product_list = create_product_objects(df)
    return product_list


@app.get("/active_products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    df = pd.read_sql("select * from product where is_active=1", engine)
    product_list = create_product_objects(df)
    return product_list


@app.get("/product_mark_ups/", response_model=List[schemas.ProductCostMarkup])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    productmark_ups = db.query(models.ProductCostMarkup).offset(skip).limit(limit).all()
    return productmark_ups


@app.get("/product_markup/{product_id}", response_model=schemas.ProductCostMarkup)
def read_product_markup(product_id: int, db: Session = Depends(get_db)):
    product_mark_up = get_product_markup(product_id, db)
    if product_mark_up:
        return product_mark_up


@app.post("/static_cost_factor/", response_model=schemas.StaticCostFactors)
def post_static_cost_factor(static_cost_factor: schemas.StaticCostFactors, db: Session = Depends(get_db)):
    return create_static_cost_factor(db, static_cost_factor)


@app.get("/static_cost_factors/", response_model=List[schemas.StaticCostFactors])
def read_static_cost_factors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    static_cpst_factors = db.query(models.StaticCostFactors).offset(skip).limit(limit).all()
    return static_cpst_factors
