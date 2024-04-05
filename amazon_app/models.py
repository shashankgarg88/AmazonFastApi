import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class Product(Base):
    __tablename__ = "product"
    id: uuid.UUID = Column(
        String,
        default=str(uuid.uuid4()),
        primary_key=True,
        index=True,
        nullable=False,
    )
    product_amazon_us_url = Column(String)
    sku = Column(String, default="")
    asin = Column(String, default="")
    title = Column(String, index=True)
    brand = Column(String)
    categories = Column(String)
    us_price = Column(String)
    us_seller = Column(String)
    is_us_prime = Column(Boolean, default=False)
    us_no_of_prime = Column(Integer)
    us_listing_count = Column(Integer)
    our_estd_min_price = Column(String)
    ca_price = Column(String)
    price_margin = Column(Float)
    ca_seller = Column(String)
    is_ca_prime = Column(Boolean, default=False)
    ca_no_of_prime = Column(Integer)
    ca_listing_count = Column(Integer)
    weight = Column(Float)
    dimension = Column(String)
    riskfactor = Column(String)
    gated = Column(String)
    is_active = Column(Boolean, default=True)

    __table_args__ = (UniqueConstraint('title', 'brand', "categories", name='_product_title_brand_category_uc'),)


class StaticCostFactors(Base):
    __tablename__ = "static_cost_factors"
    id: uuid.UUID = Column(
        String,
        default=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    fx_rate = Column(Float)
    import_duties = Column(Float)


# TABLE to track the progress of each product asin call from amazonus

class ProductCostMarkup(Base):
    __tablename__ = "product_cost_markup"
    id: uuid.UUID = Column(
        String,
        default=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    product_id = Column(Integer, ForeignKey("product.id"))
    source_price = Column(Float)
    source_price_multiplier = Column(Float)
    markup = Column(Float)
    sales_tax_rate = Column(Float)
    min_sales_markup_mul = Column(Float)
    max_sales_markup_mul = Column(Float)
    sales_markup_mul = Column(Float)
    shipping_cost = Column(Float)
    othr_variable_cost = Column(Float)
    amazon_commission_fee = Column(Float)
