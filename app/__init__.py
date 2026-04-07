from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.models import Customer, Order, OrderItem
    from app.api import api_bp
    from app.services import order_service
    
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return "Order Service API is running. Check /api/health for status."
    
    return app