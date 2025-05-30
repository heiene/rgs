"""
Round API Routes

Simple routes for round management.
All business logic is delegated to RoundService.
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.services.round_service import RoundService
from app.services.auth_service import token_required
from app.schemas.round_schema import (
    RoundCreateSchema, RoundUpdateSchema, RoundResponseSchema
)

round_api = Blueprint('round_api', __name__)

# Initialize schemas
round_create_schema = RoundCreateSchema()
round_update_schema = RoundUpdateSchema()
round_response_schema = RoundResponseSchema()


@round_api.route("/user/<int:user_id>", methods=["GET"])
@token_required
def get_user_rounds(user_id):
    """Get rounds for a user"""
    try:
        # Parse query parameters
        limit = min(int(request.args.get('limit', 20)), 100)  # Cap at 100
        
        rounds = RoundService.get_rounds_by_user(user_id, limit)
        
        return jsonify({
            "success": True,
            "data": rounds,
            "count": len(rounds),
            "user_id": user_id
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve rounds",
            "message": str(e)
        }), 500


@round_api.route("/<int:round_id>", methods=["GET"])
@token_required
def get_round(round_id):
    """Get a specific round"""
    try:
        # Parse query parameters
        include_scores = request.args.get('include_scores', 'false').lower() == 'true'
        
        round = RoundService.get_round_by_id(round_id, include_scores)
        
        if not round:
            return jsonify({
                "success": False,
                "error": "Round not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": round
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve round",
            "message": str(e)
        }), 500


@round_api.route("", methods=["POST"])
@token_required
def create_round():
    """Create a new round"""
    try:
        # Validate request data
        round_data = round_create_schema.load(request.json)
        
        # Create round via service
        round = RoundService.create_round(round_data)
        
        return jsonify({
            "success": True,
            "data": round,
            "message": "Round created successfully"
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
            "error": "Failed to create round",
            "message": str(e)
        }), 500


@round_api.route("/<int:round_id>", methods=["PUT"])
@token_required
def update_round(round_id):
    """Update an existing round"""
    try:
        # Validate request data
        round_data = round_update_schema.load(request.json)
        
        # Update round via service
        round = RoundService.update_round(round_id, round_data)
        
        if not round:
            return jsonify({
                "success": False,
                "error": "Round not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": round,
            "message": "Round updated successfully"
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
            "error": "Failed to update round",
            "message": str(e)
        }), 500


@round_api.route("/<int:round_id>", methods=["DELETE"])
@token_required
def delete_round(round_id):
    """Delete a round"""
    try:
        success = RoundService.delete_round(round_id)
        
        if not success:
            return jsonify({
                "success": False,
                "error": "Round not found"
            }), 404
            
        return jsonify({
            "success": True,
            "message": "Round deleted successfully"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to delete round",
            "message": str(e)
        }), 500


@round_api.route("/<int:round_id>/finalize", methods=["POST"])
@token_required
def finalize_round(round_id):
    """Finalize a round (calculate totals and points)"""
    try:
        round = RoundService.finalize_round(round_id)
        
        if not round:
            return jsonify({
                "success": False,
                "error": "Round not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": round,
            "message": "Round finalized successfully"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to finalize round",
            "message": str(e)
        }), 500


@round_api.route("/user/<int:user_id>/stats", methods=["GET"])
@token_required
def get_user_stats(user_id):
    """Get basic statistics for a user"""
    try:
        stats = RoundService.get_user_stats(user_id)
        
        return jsonify({
            "success": True,
            "data": stats,
            "user_id": user_id
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve user stats",
            "message": str(e)
        }), 500 