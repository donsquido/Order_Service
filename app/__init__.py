from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

# Single global SQLAlchemy + Migrate instance
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["EXPLAIN_TEMPLATE_LOADING"] = True

    # Enable CORS
    CORS(app)

    # Attach db + migrate to this app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so they are registered with SQLAlchemy
    from app import models
    from app.api import api_bp

    # Register API blueprint
    app.register_blueprint(api_bp)

    @app.route('/')
    def index():
        return "Order Service API is running. Check /api/health for status."

    # Ensure tables exist
    with app.app_context():
        db.create_all()

    return app
