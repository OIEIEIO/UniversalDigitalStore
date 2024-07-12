from flask import Blueprint, request, render_template, jsonify, send_from_directory, url_for
from sqlalchemy.orm import Session
from UniversalDigitalStore.wallet import create_subaddress, check_payment
from UniversalDigitalStore.data.products import PRODUCTS
from UniversalDigitalStore.data.models import Order, SessionLocal
import os

order_bp = Blueprint('order_bp', __name__)

def human_readable_size(size):
    """Convert size in bytes to a human-readable format."""
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

@order_bp.route('/place_order', methods=['POST'])
def place_order():
    product_id = request.form.get('product_id')
    product = PRODUCTS.get(int(product_id))
    if not product:
        return "Product not found", 404

    address = create_subaddress(product['name'])
    amount = product['price']
    download_link = f"product-{product_id}"

    # Save the order in the database
    session = SessionLocal()
    try:
        new_order = Order(
            product_id=product_id,
            product_name=product['name'],
            product_price=amount,
            payment_address=address,
            download_link=download_link
        )
        session.add(new_order)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error placing order: {e}")
        return "Internal server error", 500
    finally:
        session.close()

    return render_template('payment_details.html', address=address, amount=amount)

@order_bp.route('/orders', methods=['GET'])
def orders():
    session = SessionLocal()
    try:
        orders = session.query(Order).all()
    except Exception as e:
        print(f"Error fetching orders: {e}")
        return "Internal server error", 500
    finally:
        session.close()
    return render_template('orders.html', orders=orders)

@order_bp.route('/purchased_products', methods=['GET'])
def purchased_products():
    session = SessionLocal()
    try:
        orders = session.query(Order).filter(Order.confirmations >= 5).all()
    except Exception as e:
        print(f"Error fetching purchased products: {e}")
        return "Internal server error", 500
    finally:
        session.close()
    return render_template('purchased_products.html', orders=orders)

@order_bp.route('/api/orders', methods=['GET'])
def api_orders():
    session = SessionLocal()
    try:
        orders = session.query(Order).all()
    except Exception as e:
        print(f"Error fetching orders for API: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        session.close()

    # Convert orders to a list of dictionaries for JSON serialization
    orders_data = [
        {
            "id": order.id,
            "product_name": order.product_name,
            "product_price": order.product_price,
            "payment_address": order.payment_address,
            "confirmations": f"{order.confirmations}/5",
            "status": "Processing" if order.confirmations < 5 else "Confirmed",
            "instructions": f"https://example.com/download/{order.id}" if order.confirmations >= 5 else ""
        } for order in orders
    ]

    return jsonify(orders_data)

@order_bp.route('/api/orders/check_confirmations', methods=['GET'])
def check_confirmations():
    session = SessionLocal()
    orders = session.query(Order).filter(Order.canceled == False).all()
    response = []
    for order in orders:
        try:
            confirmations = check_payment(order.payment_address)
            if isinstance(confirmations, tuple):
                confirmations = confirmations[0]  # Assuming the first value in the tuple is the number of confirmations
            order.confirmations = int(confirmations)
            session.commit()

            response.append({
                'id': order.id,
                'product_name': order.product_name,
                'product_price': order.product_price,
                'payment_address': order.payment_address,
                'confirmations': order.confirmations,
                'status': "Confirmed" if order.confirmations >= 5 else ("Awaiting Payment" if order.confirmations == 0 else "Processing"),
                'canceled': order.canceled,
                'instructions': f"https://example.com/download/{order.id}" if order.confirmations >= 5 else ""
            })
        except Exception as e:
            session.rollback()
            print(f"Error checking payment for order {order.id}: {e}")
            response.append({
                'id': order.id,
                'product_name': order.product_name,
                'product_price': order.product_price,
                'payment_address': order.payment_address,
                'confirmations': "Error",
                'status': "Error",
                'canceled': order.canceled,
                'instructions': ""
            })
    session.close()
    return jsonify(response)

@order_bp.route('/cancel_order', methods=['POST'])
def cancel_order():
    data = request.get_json()
    order_id = data.get('order_id')
    session = SessionLocal()
    try:
        order = session.query(Order).filter(Order.id == order_id).first()
        if order and order.confirmations < 1:
            order.canceled = True
            session.commit()
        else:
            return jsonify({"message": "Order cannot be canceled"}), 400
    except Exception as e:
        session.rollback()
        print(f"Error canceling order {order_id}: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        session.close()
    return jsonify({"message": "Order canceled successfully."})

@order_bp.route('/download/<int:order_id>', methods=['GET'])
def download_file(order_id):
    session = SessionLocal()
    try:
        order = session.query(Order).filter(Order.id == order_id).first()
    except Exception as e:
        print(f"Error fetching order for download {order_id}: {e}")
        return "Internal server error", 500
    finally:
        session.close()

    if order and order.confirmations >= 5 and order.download_link:
        try:
            product_folder = os.path.join('downloads', order.download_link)
            if os.path.isdir(product_folder):
                files = os.listdir(product_folder)
                file_links = [
                    {
                        'filename': file,
                        'link': url_for('order_bp.send_file', order_id=order_id, filename=file),
                        'size': human_readable_size(os.path.getsize(os.path.join(product_folder, file)))
                    }
                    for file in files
                ]
                return render_template('download_page.html', files=file_links, order_id=order.payment_address)
            else:
                return "Product folder not found.", 404
        except Exception as e:
            print(f"Error sending file for order {order_id}: {e}")
            return "File not found or order not confirmed.", 404
    else:
        return "File not found or order not confirmed.", 404

@order_bp.route('/send_file/<int:order_id>/<filename>', methods=['GET'])
def send_file(order_id, filename):
    session = SessionLocal()
    try:
        order = session.query(Order).filter(Order.id == order_id).first()
    except Exception as e:
        print(f"Error fetching order for download {order_id}: {e}")
        return "Internal server error", 500
    finally:
        session.close()

    if order and order.confirmations >= 5 and order.download_link:
        try:
            directory = os.path.join(os.getcwd(), 'downloads', order.download_link)
            return send_from_directory(directory, filename, as_attachment=True)
        except Exception as e:
            print(f"Error sending file {filename} for order {order_id}: {e}")
            return "File not found or order not confirmed.", 404
    else:
        return "File not found or order not confirmed.", 404
