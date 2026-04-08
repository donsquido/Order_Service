import requests
import logging
from flask import current_app
from app.models import Customer, Order, OrderItem, db
from datetime import datetime
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderService:
    API_URL = "https://wrong-url.com"  # Replace with actual API endpoint
    MAX_RETRIES = 3
    
    @classmethod
    def fetch_and_store_orders(cls):
        """Fetch orders from API and store in database with deduplication"""
        for attempt in range(cls.MAX_RETRIES):
            try:
                logger.info(f"Fetching orders from API (attempt {attempt + 1})")
                response = requests.get(cls.API_URL, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                if isinstance(data, dict) and 'orders' in data:
                    orders_data = data['orders']
                else:
                    orders_data = data
                
                if not isinstance(orders_data, list):
                    raise ValueError('Unexpected orders payload format')
                
                processed_count = 0
                
                for order_data in orders_data:
                    if cls._process_single_order(order_data):
                        processed_count += 1
                
                logger.info(f"Successfully processed {processed_count} orders")
                return {"status": "success", "processed": processed_count}
                
            except requests.exceptions.RequestException as e:
                logger.error(f"API request failed (attempt {attempt + 1}): {str(e)}")
                if attempt < cls.MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error("All attempts failed.")
                    return {"status": "error", "message": str(e)}
            except Exception as e:
                logger.exception(f"Error processing orders")
                return {"status": "error", "message": str(e)}
    
    @classmethod
    def _process_single_order(cls, order_data):
        """Process single order with deduplication"""

        if not isinstance(order_data, dict):
            logger.error("Invalid order format")
            return False

        order_id = order_data.get('orderId') or order_data.get('id')
        if not order_id:
            logger.error('Order data missing order ID')
            return False
        
        # Check if order already exists (app-level idempotency)
        if Order.query.filter_by(order_id=order_id).first():
            logger.info(f"Order {order_id} already exists, skipping")
            return False
        
        try:
            # Create or get customer
            customer = cls._get_or_create_customer(order_data)
            
            # Create order
            order = Order(
                order_id=order_id,
                customer_id=customer.id,
                total_amount=order_data.get('totalAmount', order_data.get('total_price', 0)),
                status=order_data.get('status', 'pending')
            )
            db.session.add(order)
            db.session.flush()  # Get order ID
            
            # Create order items
            items = order_data.get('line_items') or order_data.get('items') or []
            for item in items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_name=item.get('productName') or item.get('sku'),
                    quantity=item.get('quantity', 1),
                    price=item.get('price', item.get('unit_price', 0))
                )
                db.session.add(order_item)
            
            # DB-level idempotency protection
            try:
                db.session.commit()
                logger.info(f"Successfully stored order {order_id}")
                return True

            except Exception as e:
                db.session.rollback()

                if "UNIQUE constraint failed" in str(e):
                    logger.warning(f"Duplicate detected at DB level for order {order_id}")
                    return False

                logger.exception(f"DB error while saving order {order_id}")
                return False
            
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Failed to process order {order_id}")
            return False
    
    @classmethod
    def _get_or_create_customer(cls, order_data):
        """Get existing customer or create new one"""
        customer_data = order_data.get('customer', {})
        email = customer_data.get('email')
        phone = customer_data.get('phone')
        
        customer = None

        if email:
            customer = Customer.query.filter_by(email=email).first()

        if not customer and phone:
            customer = Customer.query.filter_by(phone=phone).first()
        
        if not customer:
            customer = Customer(
                email=email,
                phone=phone,
                name=customer_data.get('name', 'Unknown')
            )
            db.session.add(customer)
            db.session.flush()
        
        return customer
    
    @classmethod
    def get_orders_by_customer(cls, identifier):
        """Get orders by customer email or phone"""
        from sqlalchemy import or_

        customer = Customer.query.filter(
            or_(Customer.email == identifier, Customer.phone == identifier)
        ).first()
        
        if not customer:
            return None
        
        orders = Order.query.filter_by(customer_id=customer.id).order_by(Order.created_at.desc()).all()
        
        result = {
            "customer": {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "phone": customer.phone
            },
            "orders": []
        }
        
        for order in orders:
            order_data = {
                "order_id": order.order_id,
                "total_amount": order.total_amount,
                "status": order.status,
                "created_at": order.created_at.isoformat(),
                "items": []
            }
            
            items = order.items if isinstance(order.items, list) else order.items.all()

            for item in items:
                order_data["items"].append({
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "price": item.price
                })
            
            result["orders"].append(order_data)
        
        return result


order_service = OrderService()