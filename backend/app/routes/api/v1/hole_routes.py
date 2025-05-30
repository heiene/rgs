"""
Hole API Routes

Thin routes that handle HTTP concerns only.
All business logic is delegated to HoleService.
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.services.hole_service import HoleService
from app.services.auth_service import admin_required, token_required
from app.schemas.hole_schema import (
    HoleCreateSchema, HoleUpdateSchema, HoleResponseSchema,
    StandardHolesCreateSchema, HoleStatisticsSchema, CourseValidationSchema
)

hole_api = Blueprint('hole_api', __name__)

# Initialize schemas
hole_create_schema = HoleCreateSchema()
hole_update_schema = HoleUpdateSchema()
hole_response_schema = HoleResponseSchema()
standard_holes_schema = StandardHolesCreateSchema()
hole_stats_schema = HoleStatisticsSchema()
course_validation_schema = CourseValidationSchema()


@hole_api.route("/course/<int:course_id>", methods=["GET"])
@token_required
def get_holes_by_course(course_id):
    """Get all holes for a specific course"""
    try:
        # Parse query parameters
        include_tee_positions = request.args.get('include_tee_positions', 'false').lower() == 'true'
        
        holes = HoleService.get_holes_by_course(course_id, include_tee_positions)
        
        return jsonify({
            "success": True,
            "data": holes,
            "count": len(holes),
            "course_id": course_id
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve holes",
            "message": str(e)
        }), 500


@hole_api.route("/<int:hole_id>", methods=["GET"])
@token_required
def get_hole(hole_id):
    """Get a specific hole"""
    try:
        # Parse query parameters
        include_tee_positions = request.args.get('include_tee_positions', 'false').lower() == 'true'
        
        hole = HoleService.get_hole_by_id(hole_id, include_tee_positions)
        
        if not hole:
            return jsonify({
                "success": False,
                "error": "Hole not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": hole
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve hole",
            "message": str(e)
        }), 500


@hole_api.route("", methods=["POST"])
@admin_required
def create_hole():
    """Create a new hole (admin only)"""
    try:
        # Validate request data
        hole_data = hole_create_schema.load(request.json)
        
        # Create hole via service
        hole = HoleService.create_hole(hole_data)
        
        return jsonify({
            "success": True,
            "data": hole,
            "message": "Hole created successfully"
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
            "error": "Failed to create hole",
            "message": str(e)
        }), 500


@hole_api.route("/<int:hole_id>", methods=["PUT"])
@admin_required
def update_hole(hole_id):
    """Update an existing hole (admin only)"""
    try:
        # Validate request data
        hole_data = hole_update_schema.load(request.json)
        
        # Update hole via service
        hole = HoleService.update_hole(hole_id, hole_data)
        
        if not hole:
            return jsonify({
                "success": False,
                "error": "Hole not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": hole,
            "message": "Hole updated successfully"
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
            "error": "Failed to update hole",
            "message": str(e)
        }), 500


@hole_api.route("/<int:hole_id>", methods=["DELETE"])
@admin_required
def delete_hole(hole_id):
    """Delete a hole (admin only)"""
    try:
        success = HoleService.delete_hole(hole_id)
        
        if not success:
            return jsonify({
                "success": False,
                "error": "Hole not found"
            }), 404
            
        return jsonify({
            "success": True,
            "message": "Hole deleted successfully"
        }), 200
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to delete hole",
            "message": str(e)
        }), 500


@hole_api.route("/standard", methods=["POST"])
@admin_required
def create_standard_holes():
    """Create standard 18 holes for a course (admin only)"""
    try:
        # Validate request data
        data = standard_holes_schema.load(request.json)
        
        # Create standard holes via service
        holes = HoleService.create_standard_18_holes(
            data['course_id'], 
            data.get('par_layout')
        )
        
        return jsonify({
            "success": True,
            "data": holes,
            "count": len(holes),
            "message": "Standard 18 holes created successfully"
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
            "error": "Failed to create standard holes",
            "message": str(e)
        }), 500


@hole_api.route("/<int:hole_id>/statistics", methods=["GET"])
@token_required
def get_hole_statistics(hole_id):
    """Get statistics for a specific hole"""
    try:
        stats = HoleService.get_hole_statistics(hole_id)
        
        if not stats:
            return jsonify({
                "success": False,
                "error": "Hole not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": stats
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve hole statistics",
            "message": str(e)
        }), 500


@hole_api.route("/course/<int:course_id>/validate", methods=["GET"])
@token_required
def validate_course_holes(course_id):
    """Validate hole setup for a course"""
    try:
        validation = HoleService.validate_course_holes(course_id)
        
        return jsonify({
            "success": True,
            "data": validation
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to validate course holes",
            "message": str(e)
        }), 500 