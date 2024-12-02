from flask import Blueprint, request, jsonify
from ..db import get_db_connection

import re  # For phone number validation

customer_bp = Blueprint('customer', __name__)

def validate_customer_data(data, is_update=False):
    """Validate customer data."""
    required_fields = ['firstname', 'lastname', 'phonenumber', 'address', 'city']
    if is_update:
        required_fields.append('customerid')
    for field in required_fields:
        if field not in data or not data[field].strip():
            return False, f"{field.capitalize()} is required and cannot be empty."
    # Validate phone number (must be digits only and 10 characters long)
    if not re.match(r"^\d{10}$", data['phonenumber']):
        return False, "Phone number must be 10 digits."
    return True, None

@customer_bp.route('/getcustomers', methods=['GET'])
def get_customers():
    """Retrieve all customers."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM customer")
            customers = cur.fetchall()
            return jsonify({'customers': customers}), 200
    return jsonify({'error': 'Failed to retrieve customers'}), 400

@customer_bp.route('/addcustomer', methods=['POST'])
def add_customer():
    """Add a new customer."""
    data = request.json
    valid, error_message = validate_customer_data(data)
    if not valid:
        return jsonify({'error': error_message}), 400
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO customer (firstname, lastname, phonenumber, address, city) "
                "VALUES (%s, %s, %s, %s, %s)",
                (data['firstname'], data['lastname'], data['phonenumber'], data['address'], data['city'])
            )
            conn.commit()
            return jsonify({'message': 'Customer added successfully'}), 201
    return jsonify({'error': 'Failed to add customer'}), 400

@customer_bp.route('/updatecustomer', methods=['PUT'])
def update_customer():
    """Update customer details."""
    data = request.json
    valid, error_message = validate_customer_data(data, is_update=True)
    if not valid:
        return jsonify({'error': error_message}), 400
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE customer SET firstname = %s, lastname = %s, phonenumber = %s, address = %s, city = %s "
                "WHERE customerid = %s",
                (data['firstname'], data['lastname'], data['phonenumber'], data['address'], data['city'], data['customerid'])
            )
            conn.commit()
            return jsonify({'message': 'Customer updated successfully'}), 200
    return jsonify({'error': 'Failed to update customer'}), 400

@customer_bp.route('/deletecustomer', methods=['DELETE'])
def delete_customer():
    """Delete a customer."""
    data = request.json
    if 'customerid' not in data or not str(data['customerid']).isdigit():
        return jsonify({'error': 'Valid customer ID is required'}), 400
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM customer WHERE customerid = %s", (data['customerid'],))
            conn.commit()
            return jsonify({'message': 'Customer deleted successfully'}), 200
    return jsonify({'error': 'Failed to delete customer'}), 400
