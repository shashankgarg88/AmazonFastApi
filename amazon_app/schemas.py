import uuid
from typing import List, Union, Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    title: str
    asin: str
    product_amazon_us_url: Union[str, None] = None
    sku: Union[str, None] = None
    brand: str
    categories: str
    us_price: float
    us_seller: str
    is_us_prime: bool
    us_no_of_prime: int
    us_listing_count: int
    our_estd_min_price: float
    ca_price: float
    price_margin: float
    ca_seller: Union[str, None] = None
    is_ca_prime: bool
    ca_no_of_prime: int
    ca_listing_count: int
    weight: float
    dimension: Union[str, None] = None
    riskfactor: Union[str, None] = None
    gated: Union[str, None] = None
    is_active: bool = True


class Product(ProductBase):
    id: str = uuid.uuid4()

    class Config:
        orm_mode = True


class StaticCostFactors(BaseModel):
    id: str
    fx_rate: float
    import_duties: float

    class Config:
        orm_mode = True

class ProductCostMarkup(BaseModel):
    id: str
    product_id: int
    source_price: float
    source_price_multiplier: float
    markup: float
    sales_tax_rate: float
    min_sales_markup_mul: float
    max_sales_markup_mul: float
    sales_markup_mul: float
    shipping_cost: float
    othr_variable_cost: float
    amazon_commission_fee: float

    class Config:
        orm_mode = True

