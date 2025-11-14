from .main import main_bp
from .client import client_bp
from .product import product_bp
from .admin import admin_bp

def init_routes(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(admin_bp)
