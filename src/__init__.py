from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.config_db.db import Config_db
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_class=Config_db,):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    CORS(app)

    from src.route.produtos.route import init_routeClients
    from src.route.clientes.route import init_routeProduct
    init_routeProduct(app)
    init_routeClients(app)
    return app