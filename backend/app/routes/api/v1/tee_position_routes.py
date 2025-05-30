"""
TeePosition API Routes

Thin routes that handle HTTP concerns only.
All business logic is delegated to TeePositionService.
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.services.tee_position_service import TeePositionService
from app.services.auth_service import admin_required, token_required
from app.schemas.tee_position_schema import (
    TeePositionCreateSchema, TeePositionUpdateSchema, TeePositionResponseSchema,
    TeePositionBulkCreateSchema, StandardDistancesCreateSchema,
    TeePositionBulkUpdateSchema, TeePositionStatisticsSchema, UnitQuerySchema
)

tee_position_api = Blueprint('tee_position_api', __name__)

# Initialize schemas
tee_position_create_schema = TeePositionCreateSchema()
tee_position_update_schema = TeePositionUpdateSchema()
tee_position_response_schema = TeePositionResponseSchema()
bulk_create_schema = TeePositionBulkCreateSchema()
standard_distances_schema = StandardDistancesCreateSchema()
bulk_update_schema = TeePositionBulkUpdateSchema()
statistics_schema = TeePositionStatisticsSchema()
unit_query_schema = UnitQuerySchema()


@tee_position_api.route("/tee-set/<int:tee_set_id>", methods=["GET"])
@token_required
def get_tee_positions_by_tee_set(tee_set_id):
    """Get all tee positions for a specific tee set"""
    try:
        # Parse query parameters
        unit = request.args.get('unit', 'meters')
        if unit not in ['meters', 'yards']:
            return jsonify({
                "success": False,
                "error": "Unit must be 'meters' or 'yards'"
            }), 400
        
        positions = TeePositionService.get_tee_positions_by_tee_set(tee_set_id, unit)
        
        return jsonify({
            "success": True,
            "data": positions,
            "count": len(positions),
            "tee_set_id": tee_set_id,
            "unit": unit
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve tee positions",
            "message": str(e)
        }), 500


@tee_position_api.route("/hole/<int:hole_id>", methods=["GET"])
@token_required
def get_tee_positions_by_hole(hole_id):
    """Get all tee positions for a specific hole"""
    try:
        # Parse query parameters
        unit = request.args.get('unit', 'meters')
        if unit not in ['meters', 'yards']:
            return jsonify({
                "success": False,
                "error": "Unit must be 'meters' or 'yards'"
            }), 400
        
        positions = TeePositionService.get_tee_positions_by_hole(hole_id, unit)
        
        return jsonify({
            "success": True,
            "data": positions,
            "count": len(positions),
            "hole_id": hole_id,
            "unit": unit
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve tee positions",
            "message": str(e)
        }), 500


@tee_position_api.route("/<int:position_id>", methods=["GET"])
@token_required
def get_tee_position(position_id):
    """Get a specific tee position"""
    try:
        # Parse query parameters
        unit = request.args.get('unit', 'meters')
        if unit not in ['meters', 'yards']:
            return jsonify({
                "success": False,
                "error": "Unit must be 'meters' or 'yards'"
            }), 400
        
        position = TeePositionService.get_tee_position_by_id(position_id, unit)
        
        if not position:
            return jsonify({
                "success": False,
                "error": "Tee position not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": position
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve tee position",
            "message": str(e)
        }), 500


@tee_position_api.route("", methods=["POST"])
@admin_required
def create_tee_position():
    """Create a new tee position (admin only)"""
    try:
        # Validate request data
        position_data = tee_position_create_schema.load(request.json)
        
        # Create tee position via service
        position = TeePositionService.create_tee_position(position_data)
        
        return jsonify({
            "success": True,
            "data": position,
            "message": "Tee position created successfully"
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
            "error": "Failed to create tee position",
            "message": str(e)
        }), 500


@tee_position_api.route("/<int:position_id>", methods=["PUT"])
@admin_required
def update_tee_position(position_id):
    """Update an existing tee position (admin only)"""
    try:
        # Validate request data
        position_data = tee_position_update_schema.load(request.json)
        
        # Update tee position via service
        position = TeePositionService.update_tee_position(position_id, position_data)
        
        if not position:
            return jsonify({
                "success": False,
                "error": "Tee position not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": position,
            "message": "Tee position updated successfully"
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
            "error": "Failed to update tee position",
            "message": str(e)
        }), 500


@tee_position_api.route("/<int:position_id>", methods=["DELETE"])
@admin_required
def delete_tee_position(position_id):
    """Delete a tee position (admin only)"""
    try:
        success = TeePositionService.delete_tee_position(position_id)
        
        if not success:
            return jsonify({
                "success": False,
                "error": "Tee position not found"
            }), 404
            
        return jsonify({
            "success": True,
            "message": "Tee position deleted successfully"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to delete tee position",
            "message": str(e)
        }), 500


@tee_position_api.route("/bulk", methods=["POST"])
@admin_required
def create_bulk_tee_positions():
    """Create tee positions for all holes in a tee set (admin only)"""
    try:
        # Validate request data
        data = bulk_create_schema.load(request.json)
        
        # Create tee positions via service
        positions = TeePositionService.create_tee_positions_for_tee_set(
            data['tee_set_id'], 
            data['distances']
        )
        
        return jsonify({
            "success": True,
            "data": positions,
            "count": len(positions),
            "message": "Tee positions created successfully"
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
            "error": "Failed to create tee positions",
            "message": str(e)
        }), 500


@tee_position_api.route("/standard", methods=["POST"])
@admin_required
def create_standard_distances():
    """Create standard distances based on par and difficulty (admin only)"""
    try:
        # Validate request data
        data = standard_distances_schema.load(request.json)
        
        # Create standard distances via service
        positions = TeePositionService.create_standard_distances_by_par(
            data['tee_set_id'], 
            data['difficulty_level']
        )
        
        return jsonify({
            "success": True,
            "data": positions,
            "count": len(positions),
            "difficulty_level": data['difficulty_level'],
            "message": "Standard tee positions created successfully"
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
            "error": "Failed to create standard distances",
            "message": str(e)
        }), 500


@tee_position_api.route("/tee-set/<int:tee_set_id>/statistics", methods=["GET"])
@token_required
def get_tee_position_statistics(tee_set_id):
    """Get statistics for tee positions of a tee set"""
    try:
        stats = TeePositionService.get_tee_position_statistics(tee_set_id)
        
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
            "error": "Failed to retrieve tee position statistics",
            "message": str(e)
        }), 500


@tee_position_api.route("/bulk-update", methods=["PUT"])
@admin_required
def bulk_update_distances():
    """Bulk update distances for a tee set (admin only)"""
    try:
        # Validate request data
        data = bulk_update_schema.load(request.json)
        
        # Bulk update distances via service
        positions = TeePositionService.bulk_update_distances(
            data['tee_set_id'], 
            data['distances']
        )
        
        return jsonify({
            "success": True,
            "data": positions,
            "count": len(positions),
            "message": "Distances updated successfully"
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
            "error": "Failed to update distances",
            "message": str(e)
        }), 500 