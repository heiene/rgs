"""
TeeSet API Routes

Thin routes that handle HTTP concerns only.
All business logic is delegated to TeeSetService.
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.services.tee_set_service import TeeSetService
from app.services.auth_service import admin_required, token_required
from app.schemas.tee_set_schema import (
    TeeSetCreateSchema, TeeSetUpdateSchema, TeeSetResponseSchema,
    StandardTeeSetsCreateSchema, GenderRatingQuerySchema, 
    TeeSetStatisticsSchema, TeeSetValidationSchema
)

tee_set_api = Blueprint('tee_set_api', __name__)

# Initialize schemas
tee_set_create_schema = TeeSetCreateSchema()
tee_set_update_schema = TeeSetUpdateSchema()
tee_set_response_schema = TeeSetResponseSchema()
standard_tee_sets_schema = StandardTeeSetsCreateSchema()
gender_rating_schema = GenderRatingQuerySchema()
tee_set_stats_schema = TeeSetStatisticsSchema()
tee_set_validation_schema = TeeSetValidationSchema()


@tee_set_api.route("/course/<int:course_id>", methods=["GET"])
@token_required
def get_tee_sets_by_course(course_id):
    """Get all tee sets for a specific course"""
    try:
        # Parse query parameters
        include_positions = request.args.get('include_positions', 'false').lower() == 'true'
        
        tee_sets = TeeSetService.get_tee_sets_by_course(course_id, include_positions)
        
        return jsonify({
            "success": True,
            "data": tee_sets,
            "count": len(tee_sets),
            "course_id": course_id
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve tee sets",
            "message": str(e)
        }), 500


@tee_set_api.route("/<int:tee_set_id>", methods=["GET"])
@token_required
def get_tee_set(tee_set_id):
    """Get a specific tee set"""
    try:
        # Parse query parameters
        include_positions = request.args.get('include_positions', 'false').lower() == 'true'
        
        tee_set = TeeSetService.get_tee_set_by_id(tee_set_id, include_positions)
        
        if not tee_set:
            return jsonify({
                "success": False,
                "error": "Tee set not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": tee_set
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve tee set",
            "message": str(e)
        }), 500


@tee_set_api.route("", methods=["POST"])
@admin_required
def create_tee_set():
    """Create a new tee set (admin only)"""
    try:
        # Validate request data
        tee_set_data = tee_set_create_schema.load(request.json)
        
        # Create tee set via service
        tee_set = TeeSetService.create_tee_set(tee_set_data)
        
        return jsonify({
            "success": True,
            "data": tee_set,
            "message": "Tee set created successfully"
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
            "error": "Failed to create tee set",
            "message": str(e)
        }), 500


@tee_set_api.route("/<int:tee_set_id>", methods=["PUT"])
@admin_required
def update_tee_set(tee_set_id):
    """Update an existing tee set (admin only)"""
    try:
        # Validate request data
        tee_set_data = tee_set_update_schema.load(request.json)
        
        # Update tee set via service
        tee_set = TeeSetService.update_tee_set(tee_set_id, tee_set_data)
        
        if not tee_set:
            return jsonify({
                "success": False,
                "error": "Tee set not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": tee_set,
            "message": "Tee set updated successfully"
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
            "error": "Failed to update tee set",
            "message": str(e)
        }), 500


@tee_set_api.route("/<int:tee_set_id>", methods=["DELETE"])
@admin_required
def delete_tee_set(tee_set_id):
    """Delete a tee set (admin only)"""
    try:
        success = TeeSetService.delete_tee_set(tee_set_id)
        
        if not success:
            return jsonify({
                "success": False,
                "error": "Tee set not found"
            }), 404
            
        return jsonify({
            "success": True,
            "message": "Tee set deleted successfully"
        }), 200
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to delete tee set",
            "message": str(e)
        }), 500


@tee_set_api.route("/standard", methods=["POST"])
@admin_required
def create_standard_tee_sets():
    """Create standard tee sets for a course (admin only)"""
    try:
        # Validate request data
        data = standard_tee_sets_schema.load(request.json)
        
        # Create standard tee sets via service
        tee_sets = TeeSetService.create_standard_tee_sets(data['course_id'])
        
        return jsonify({
            "success": True,
            "data": tee_sets,
            "count": len(tee_sets),
            "message": "Standard tee sets created successfully"
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
            "error": "Failed to create standard tee sets",
            "message": str(e)
        }), 500


@tee_set_api.route("/<int:tee_set_id>/rating", methods=["GET"])
@token_required
def get_tee_set_rating(tee_set_id):
    """Get tee set rating for specific gender"""
    try:
        # Parse query parameters
        gender = request.args.get('gender', 'M')
        
        # Validate gender parameter
        if gender not in ['M', 'F']:
            return jsonify({
                "success": False,
                "error": "Gender must be 'M' or 'F'"
            }), 400
        
        rating = TeeSetService.get_rating_for_gender(tee_set_id, gender)
        
        if not rating:
            return jsonify({
                "success": False,
                "error": "Tee set not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": {
                "tee_set_id": tee_set_id,
                "gender": gender,
                **rating
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve tee set rating",
            "message": str(e)
        }), 500


@tee_set_api.route("/<int:tee_set_id>/statistics", methods=["GET"])
@token_required
def get_tee_set_statistics(tee_set_id):
    """Get statistics for a specific tee set"""
    try:
        stats = TeeSetService.get_tee_set_statistics(tee_set_id)
        
        if not stats:
            return jsonify({
                "success": False,
                "error": "Tee set not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": stats
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve tee set statistics",
            "message": str(e)
        }), 500


@tee_set_api.route("/course/<int:course_id>/validate", methods=["GET"])
@token_required
def validate_tee_set_setup(course_id):
    """Validate tee set setup for a course"""
    try:
        validation = TeeSetService.validate_tee_set_setup(course_id)
        
        return jsonify({
            "success": True,
            "data": validation
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to validate tee set setup",
            "message": str(e)
        }), 500 