"""
API v1 Blueprint
"""
from flask import Blueprint, jsonify
from datetime import datetime

# Create API v1 blueprint
api_v1_bp = Blueprint('api_v1', __name__)

# Health check endpoint for API
@api_v1_bp.route('/health')
def api_health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'rgs-api',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# Import and register route blueprints
from .auth_routes import auth_bp
from .user_routes import user_bp
from .handicap_routes import handicap_bp
from .club_routes import club_api
from .theme_routes import theme_api
from .course_routes import course_api
from .hole_routes import hole_api
from .tee_set_routes import tee_set_api
from .tee_position_routes import tee_position_api
from .round_routes import round_api
from .score_routes import score_api

api_v1_bp.register_blueprint(auth_bp, url_prefix='/auth')
api_v1_bp.register_blueprint(user_bp, url_prefix='/users')
api_v1_bp.register_blueprint(handicap_bp, url_prefix='/handicaps')
api_v1_bp.register_blueprint(club_api, url_prefix='/clubs')
api_v1_bp.register_blueprint(theme_api, url_prefix='/themes')
api_v1_bp.register_blueprint(course_api, url_prefix='/courses')
api_v1_bp.register_blueprint(hole_api, url_prefix='/holes')
api_v1_bp.register_blueprint(tee_set_api, url_prefix='/tee-sets')
api_v1_bp.register_blueprint(tee_position_api, url_prefix='/tee-positions')
api_v1_bp.register_blueprint(round_api, url_prefix='/rounds')
api_v1_bp.register_blueprint(score_api, url_prefix='/scores') 