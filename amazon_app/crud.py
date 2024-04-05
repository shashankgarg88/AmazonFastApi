import uuid

from sqlalchemy.orm import Session

import pandas as pd
from . import models, schemas
from .constants import column_mapping, numeric_colums
from .database import SQLALCHEMY_DATABASE_URL, engine
from .schemas import Product
from .sql_wrapper import ProductsDBMapper


def insert_products(df: pd.DataFrame, db: Session):
    db_mapper = ProductsDBMapper(
        connection_string=SQLALCHEMY_DATABASE_URL,
        sql_table_name="product",
    )
    db_mapper.insert_dataframe_into_database(df)


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_products(db: Session, data: pd.DataFrame):
    data['id'] = [str(uuid.uuid4()) for _ in range(len(data.index))]
    product_list = create_product_objects(data)
    db.add_all(product_list)
    db.commit()
    # db.refresh(products)
    return product_list


def map_products(data: dict):
    product = Product(**data)
    return product


def create_product_objects(data: pd.DataFrame):
    product_list = []

    for record in data.to_dict('records'):
        data_obj = models.Product(**record)
        product_list.append(data_obj)
    return product_list


def get_product_markup(product_id: int, db: Session):
    return db.query(models.ProductCostMarkup).filter(models.ProductCostMarkup.product_id == product_id).first()


def create_static_cost_factor(db: Session, data: schemas.StaticCostFactors):
    static_cost_factor = models.StaticCostFactors(**data.model_dump())
    db.add(static_cost_factor)
    db.commit()
    db.refresh(static_cost_factor)
    return static_cost_factor


def get_static_cost_factors(row_id: int, db: Session):
    return db.query(models.StaticCostFactors).filter(models.StaticCostFactors.id == row_id).first()


def bulk_update_products(df: pd.DataFrame):
    products_from_db = pd.read_sql("select * from product;", engine)
    products_from_db.set_index(keys=["asin"], inplace=True)
    df.set_index(keys=["asin"], inplace=True)
    products_from_db.update(df)
    products_from_db.to_sql("product", engine, if_exists="replace")
    products_from_db.reset_index()
    return products_from_db


def transform_excel_data(df: pd.DataFrame):
    df = df.rename(columns=column_mapping)

    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    string_columns = list(set(column_mapping.values()) - set(numeric_colums))
    df[numeric_colums].apply(pd.to_numeric, errors="coerce", axis=1)
    for col in numeric_colums:
        df[col] = df[col].astype(float)
    df[string_columns] = df[string_columns].fillna("")
    df[numeric_colums] = df[numeric_colums].fillna(0)
    df = df.drop_duplicates(subset=["title", "brand", "categories"])

    return df
