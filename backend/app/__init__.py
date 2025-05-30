"""
Flask application factory
"""
from flask import Flask
from flask_cors import CORS
from app.extensions import db, ma, login_manager, migrate, jwt, mail
from app.config import config


def create_app(config_name='development'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    
    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {"origins": "*"},
        r"/health": {"origins": "*"}
    })
    
    # Register blueprints
    register_blueprints(app)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'flask-backend'}, 200
    
    return app


def register_blueprints(app):
    """Register application blueprints"""
    # API routes
    from app.routes.api.v1 import api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')
    
    # Admin web routes
    from app.routes.web import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin') 