# data/products.py
PRODUCTS = {
    1: {"name": "Digital Download", "price": 0.0001},
    2: {"name": "E-Book Access", "price": 0.00012},
    3: {"name": "Online Course", "price": 0.000123}
}

def get_product(product_id):
    return PRODUCTS.get(product_id, None)
