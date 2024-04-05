from amazon_app.database import SQLALCHEMY_DATABASE_URL
from amazon_app.schemas import Product, ProductBase
from amazon_app.sql_wrapper import ProductsDBMapper

old_column_names = ['title', 'Brand', 'categories', ' us price ', 'us seller', 'us prime ?', 'us no of prime',
                    'us listing cnt', ' our est min price ', ' ca price ', ' Price Margin ', 'ca seller', 'ca prime ?',
                    'ca no of prime', 'ca listing count', 'weight', 'dimension', 'RiskFactor', 'Gated']

new_column_names = ["title", "brand", "categories", "us_price", "us_seller", "is_us_prime", "us_no_of_prime",
                    "us_listing_count", "our_estd_min_price", "ca_price", "price_margin", "ca_seller", "is_ca_prime",
                    "ca_no_of_prime", "ca_listing_count", "weight", "dimension", "riskfactor", "gated"]

import pandas as pd

column_mapping = {'title': 'title', 'Brand': 'brand', 'categories': 'categories', 'us price': 'us_price',
                  'us seller': 'us_seller', 'us prime ?': 'is_us_prime', 'us no of prime': 'us_no_of_prime',
                  'us listing cnt': 'us_listing_count', 'our est min price': 'our_estd_min_price',
                  'ca price': 'ca_price', 'Price Margin': 'price_margin', 'ca seller': 'ca_seller',
                  'ca prime ?': 'is_ca_prime', 'ca no of prime': 'ca_no_of_prime',
                  'ca listing count': 'ca_listing_count', 'weight': 'weight', 'dimension': 'dimension',
                  'RiskFactor': 'riskfactor', 'Gated': 'gated'}


def map_products(data:dict):
    product = ProductBase(**data)
    return product

product_data = pd.read_excel("/Users/shashankgarg/PycharmProjects/AmazonFastApi/Testz_File_Amazon.xlsx", sheet_name=None, engine='openpyxl')

df = product_data['Sheet2']
# df = pd.read_csv("/Users/shashankgarg/PycharmProjects/AmazonFastApi/Test_File_Amazon.csv")
df = df.rename(columns=column_mapping)


# df["ca_price"] = df["ca_price"].apply(
#     lambda x: x.remove.strip()
# )
# df["us_price"] = df["us_price"].astype(str).apply(
#     lambda x: x.split("$")[1].strip()
# ).replace("-", "0")
# df["our_estd_min_price"] = df["our_estd_min_price"].apply(
#     lambda x: x.split("$")[1].strip()
# ).replace("-", "0")
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

numeric_colums = [
    "us_price",
    "is_us_prime",
    "us_no_of_prime",
    "us_listing_count",
    "our_estd_min_price",
    "ca_price",
    "price_margin",
    "is_ca_prime",
    "ca_no_of_prime",
    "ca_listing_count",
    "weight",
]
string_columns = list(set(column_mapping.values()) - set(numeric_colums))
df[numeric_colums].apply(pd.to_numeric, errors="coerce", axis=1)
for col in numeric_colums:
    df[col] = df[col].astype(float)
df[string_columns] = df[string_columns].fillna("")
product_list = map(map_products, df.to_dict('records'))
products = list(product_list)
# db_mapper.insert_dataframe_into_database(df)
print()
