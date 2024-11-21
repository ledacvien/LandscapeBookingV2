from flask import Blueprint, request, jsonify
from ..db import get_db_connection

order_bp = Blueprint('order', __name__)

status_list = ['Scheduled', 'In-progress', 'Completed']

@order_bp.route('/getorders', methods=['GET'])
def get_orders():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM orders")
            orders = cur.fetchall()
            return jsonify({'orders': orders}), 200
    return jsonify({'error': 'Database error'}), 400

@order_bp.route('/getstatuslist', methods=['GET'])
def get_status_list():
    return jsonify({'status_list': status_list}), 200

# Define JSON
# {
#     "customerid": 1,
#     "teamid": 1,
#     "status": "Scheduled"
# }
@order_bp.route('/addorder', methods=['POST'])
def add_order():
    data = request.json
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Check if customer and team exist
            cur.execute("SELECT 1 FROM customer WHERE customerid = %s", (data['customerid'],))
            if not cur.fetchone():
                return jsonify({'error': 'Customer does not exist'}), 400
            cur.execute("SELECT 1 FROM team WHERE teamid = %s", (data['teamid'],))
            if not cur.fetchone():
                return jsonify({'error': 'Team does not exist'}), 400
            
            # Add order
            cur.execute("INSERT INTO orders (customerid, teamid, status) VALUES (%s, %s, %s)",
                        (data['customerid'], data['teamid'], data['status']))
            conn.commit()
            return jsonify({'message': 'Order added successfully'}), 201
    return jsonify({'error': 'Failed to add order. Database error'}), 400

# Define JSON
# {
#     "ordernumber": 1,
#     "customerid": 1,
#     "teamid": 1,
#     "status": "In-progress"
# }
@order_bp.route('/updateorder', methods=['PUT'])
def update_order():
    data = request.json
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Check if customer and team exist
            cur.execute("SELECT 1 FROM customer WHERE customerid = %s", (data['customerid'],))
            if not cur.fetchone():
                return jsonify({'error': 'Customer does not exist'}), 400
            cur.execute("SELECT 1 FROM team WHERE teamid = %s", (data['teamid'],))
            if not cur.fetchone():
                return jsonify({'error': 'Team does not exist'}), 400
            
            # Update order
            cur.execute("UPDATE orders SET customerid = %s, teamid = %s, status = %s WHERE ordernumber = %s",
                        (data['customerid'], data['teamid'], data['status'], data['ordernumber']))
            conn.commit()
            return jsonify({'message': 'Order updated successfully'}), 200
    return jsonify({'error': 'Failed to update order. Database error'}), 400

# Define JSON
# {
#     "ordernumber": 1
# }
@order_bp.route('/deleteorder', methods=['DELETE'])
def delete_order():
    data = request.json
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM orders WHERE ordernumber = %s", (data['ordernumber'],))
            conn.commit()
            return jsonify({'message': 'Order deleted successfully'})
    return jsonify({'error': 'Failed to delete order. Database error'}), 400