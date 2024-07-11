from data.db import SessionLocal
from data.models import Order

def create_order(product_id, address, amount):
    session = SessionLocal()
    new_order = Order(product_id=product_id, address=address, amount=amount)
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    session.close()
    return new_order

def get_orders():
    session = SessionLocal()
    orders = session.query(Order).all()
    session.close()
    return orders

def update_order_status(order_id, status):
    session = SessionLocal()
    order = session.query(Order).filter(Order.id == order_id).first()
    if order:
        order.status = status
        session.commit()
        session.refresh(order)
    session.close()
    return order
