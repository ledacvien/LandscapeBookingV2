from flask import Blueprint

from .order_routes import order_bp
from .city_routes import city_bp
from .customer_routes import customer_bp
from .team_routes import team_bp

def register_routes(app):
    app.register_blueprint(order_bp, url_prefix='/api/order')
    app.register_blueprint(city_bp, url_prefix='/api/city')
    app.register_blueprint(customer_bp, url_prefix='/api/customer')
    app.register_blueprint(team_bp, url_prefix='/api/team')