"""
Admin Web Blueprint
"""
from flask import Blueprint

# Create admin blueprint
admin_bp = Blueprint('admin', __name__)

# Import routes to register them with the blueprint
from . import admin_routes 