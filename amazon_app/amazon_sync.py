from amazon_app import schemas


def get_product_price_amazon_us(asin:str, run_only_active_products= False):
    """
    Get price & quantity of the product from amazom.us on product asin.
    - If quantity is 0, mark the product on amanzaon ca as inactive or update quantity as 0

    :param asin:
    :return:
    """
    # TODO:- Get sample response of the Amanzon.us api against ASIN- Sunny
    pass



def calculate_product_markup(product: schemas.Product, static_cost_factor: schemas.StaticCostFactors, product_markup:schemas.ProductCostMarkup):


    pass