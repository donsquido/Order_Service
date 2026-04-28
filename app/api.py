from flask import Blueprint, jsonify, request, render_template
from app.services import order_service
import logging

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)


@api_bp.route('/ingest-orders', methods=['POST'])
def ingest_orders():
    """Endpoint to fetch and store orders from external API"""
    logger.info("Ingest orders endpoint called")

    result = order_service.fetch_and_store_orders()

    return jsonify(result), 200 if result['status'] == 'success' else 500


@api_bp.route('/customer/<identifier>', methods=['GET'])
def get_customer_orders(identifier):
    """Get customer orders by email or phone (path param version)"""
    logger.info(f"Fetching orders for customer: {identifier}")

    data = order_service.get_orders_by_customer(identifier)

    if not data:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify(data), 200


@api_bp.route('/orders', methods=['GET'])
def get_orders():
    """Get orders by email or phone (query param version)"""
    email = request.args.get("email")
    phone = request.args.get("phone")

    identifier = email or phone

    if not identifier:
        return jsonify({"error": "Email or phone is required"}), 400

    logger.info(f"Fetching orders using query param: {identifier}")

    data = order_service.get_orders_by_customer(identifier)

    if not data:
        return render_template("404.html"), 404


    return render_template("orders.html", data=data)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Lightweight health check endpoint"""
    return jsonify({"status": "OK"}), 200


# UI HOME PAGE
@api_bp.route('/')
def home_page():
    """Home page - auto fetch and display sample customer"""

    order_service.fetch_and_store_orders()

    raw_data = order_service.get_orders_by_customer("thomas@avantcha.com")

    if not raw_data:
        return render_template("error.html", message="Customer not found")

    return render_template("index.html", data=raw_data)


# VIEW ORDERS (EMAIL / PHONE)
@api_bp.route('/view-orders')
def view_orders_page():
    """View orders page via email or phone"""

    email = request.args.get("email")
    phone = request.args.get("phone")

    identifier = email or phone

    if not identifier:
        return render_template("error.html", message="Email or phone required")

    raw_data = order_service.get_orders_by_customer(identifier)

    if not raw_data:
        return render_template("error.html", message="Customer not found")

    # ✅ Ensure structure matches UI expectation
    formatted_data = {
        "customer": {
    "name": raw_data.get("customer", {}).get("name"),
    "email": raw_data.get("customer", {}).get("email"),
    "phone": raw_data.get("customer", {}).get("phone"),
},
        "orders": []
    }

    for order in raw_data.get("orders", []):
        formatted_order = {
            "order_id": order.get("order_id"),
            "total_amount": order.get("total") or order.get("total_amount"),
            "status": order.get("status"),
            "items": order.get("items", [])
        }
        formatted_data["orders"].append(formatted_order)

    return render_template("orders.html", data=formatted_data)