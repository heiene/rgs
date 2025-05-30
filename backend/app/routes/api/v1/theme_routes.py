"""
Theme API Routes

Thin routes that handle HTTP concerns only.
All business logic is delegated to ThemeService.
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.services.theme_service import ThemeService
from app.services.auth_service import admin_required, token_required
from app.schemas.theme_schema import (
    ThemeCreateSchema, ThemeUpdateSchema, ThemeResponseSchema
)

theme_api = Blueprint('theme_api', __name__)

# Initialize schemas
theme_create_schema = ThemeCreateSchema()
theme_update_schema = ThemeUpdateSchema()
theme_response_schema = ThemeResponseSchema()


@theme_api.route("", methods=["GET"])
@token_required
def list_themes():
    """Get all themes - requires authentication"""
    try:
        themes = ThemeService.get_all_themes()
            
        return jsonify({
            "success": True,
            "data": themes,
            "count": len(themes)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve themes",
            "message": str(e)
        }), 500


@theme_api.route("/<int:theme_id>", methods=["GET"])
@token_required
def get_theme(theme_id):
    """Get a specific theme - requires authentication"""
    try:
        theme = ThemeService.get_theme_by_id(theme_id)
            
        if not theme:
            return jsonify({
                "success": False,
                "error": "Theme not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": theme
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve theme",
            "message": str(e)
        }), 500


@theme_api.route("", methods=["POST"])
@admin_required
def create_theme():
    """Create a new theme (admin only)"""
    try:
        # Validate request data
        theme_data = theme_create_schema.load(request.json)
        
        # Create theme via service
        theme = ThemeService.create_theme(theme_data)
        
        return jsonify({
            "success": True,
            "data": theme,
            "message": "Theme created successfully"
        }), 201
        
    except ValidationError as e:
        return jsonify({
            "success": False,
            "error": "Validation failed",
            "details": e.messages
        }), 400
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to create theme",
            "message": str(e)
        }), 500


@theme_api.route("/<int:theme_id>", methods=["PUT"])
@admin_required
def update_theme(theme_id):
    """Update an existing theme (admin only)"""
    try:
        # Validate request data
        theme_data = theme_update_schema.load(request.json)
        
        # Update theme via service
        theme = ThemeService.update_theme(theme_id, theme_data)
        
        if not theme:
            return jsonify({
                "success": False,
                "error": "Theme not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": theme,
            "message": "Theme updated successfully"
        }), 200
        
    except ValidationError as e:
        return jsonify({
            "success": False,
            "error": "Validation failed",
            "details": e.messages
        }), 400
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to update theme",
            "message": str(e)
        }), 500


@theme_api.route("/<int:theme_id>", methods=["DELETE"])
@admin_required
def delete_theme(theme_id):
    """Delete a theme (admin only)"""
    try:
        success = ThemeService.delete_theme(theme_id)
        
        if not success:
            return jsonify({
                "success": False,
                "error": "Theme not found"
            }), 404
            
        return jsonify({
            "success": True,
            "message": "Theme deleted successfully"
        }), 200
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to delete theme",
            "message": str(e)
        }), 500


@theme_api.route("/defaults", methods=["POST"])
@admin_required
def create_default_themes():
    """Create default themes (admin only)"""
    try:
        created_themes = ThemeService.create_default_themes()
        
        return jsonify({
            "success": True,
            "data": created_themes,
            "count": len(created_themes),
            "message": f"Created {len(created_themes)} default themes"
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to create default themes",
            "message": str(e)
        }), 500 