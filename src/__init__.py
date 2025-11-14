from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.config_db.db import Config_db
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_class=Config_db):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    
    from .route import init_routes
    init_routes(app)

    CORS(app)

    return app
