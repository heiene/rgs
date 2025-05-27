"""
API v1 Blueprint
"""
from flask import Blueprint

# Create API v1 blueprint
api_v1_bp = Blueprint('api_v1', __name__)

# Import routes to register them with the blueprint
from . import auth_routes, user_routes 