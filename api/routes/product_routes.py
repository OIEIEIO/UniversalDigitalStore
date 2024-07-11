from flask import Blueprint, jsonify

product_bp = Blueprint('products', __name__)

PRODUCTS = {
    1: {"name": "Digital Download", "price": 0.0001},
    2: {"name": "E-Book Access", "price": 0.0001},
    3: {"name": "Online Course", "price": 0.0001}
}

@product_bp.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(PRODUCTS)

@product_bp.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = PRODUCTS.get(product_id)
    if product:
        return jsonify(product)
    else:
        return "Product not found", 404
