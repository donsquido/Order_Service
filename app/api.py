from flask import Blueprint, jsonify, request
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
    
    customer_data = order_service.get_orders_by_customer(identifier)
    
    if not customer_data:
        return jsonify({"error": "Customer not found"}), 404
    
    return jsonify(customer_data)


@api_bp.route('/orders', methods=['GET'])
def get_orders():
    """Get orders by email or phone (query param version)"""
    email = request.args.get("email")
    phone = request.args.get("phone")

    identifier = email or phone

    if not identifier:
        return jsonify({"error": "Email or phone is required"}), 400

    logger.info(f"Fetching orders using query param: {identifier}")

    customer_data = order_service.get_orders_by_customer(identifier)

    if not customer_data:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify(customer_data), 200


@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200