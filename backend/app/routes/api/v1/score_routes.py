"""
Score API Routes

Simple routes for score management.
All business logic is delegated to ScoreService.
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.services.score_service import ScoreService
from app.services.auth_service import token_required
from app.schemas.score_schema import (
    ScoreCreateSchema, ScoreUpdateSchema, ScoreResponseSchema,
    BulkScoreCreateSchema
)

score_api = Blueprint('score_api', __name__)

# Initialize schemas
score_create_schema = ScoreCreateSchema()
score_update_schema = ScoreUpdateSchema()
score_response_schema = ScoreResponseSchema()
bulk_score_schema = BulkScoreCreateSchema()


@score_api.route("/round/<int:round_id>", methods=["GET"])
@token_required
def get_round_scores(round_id):
    """Get all scores for a round"""
    try:
        scores = ScoreService.get_scores_by_round(round_id)
        
        return jsonify({
            "success": True,
            "data": scores,
            "count": len(scores),
            "round_id": round_id
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve scores",
            "message": str(e)
        }), 500


@score_api.route("/<int:score_id>", methods=["GET"])
@token_required
def get_score(score_id):
    """Get a specific score"""
    try:
        score = ScoreService.get_score_by_id(score_id)
        
        if not score:
            return jsonify({
                "success": False,
                "error": "Score not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": score
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve score",
            "message": str(e)
        }), 500


@score_api.route("", methods=["POST"])
@token_required
def create_score():
    """Create a new score"""
    try:
        # Validate request data
        score_data = score_create_schema.load(request.json)
        
        # Create score via service
        score = ScoreService.create_score(score_data)
        
        return jsonify({
            "success": True,
            "data": score,
            "message": "Score created successfully"
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
            "error": "Failed to create score",
            "message": str(e)
        }), 500


@score_api.route("/<int:score_id>", methods=["PUT"])
@token_required
def update_score(score_id):
    """Update an existing score"""
    try:
        # Validate request data
        score_data = score_update_schema.load(request.json)
        
        # Update score via service
        score = ScoreService.update_score(score_id, score_data)
        
        if not score:
            return jsonify({
                "success": False,
                "error": "Score not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": score,
            "message": "Score updated successfully"
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
            "error": "Failed to update score",
            "message": str(e)
        }), 500


@score_api.route("/<int:score_id>", methods=["DELETE"])
@token_required
def delete_score(score_id):
    """Delete a score"""
    try:
        success = ScoreService.delete_score(score_id)
        
        if not success:
            return jsonify({
                "success": False,
                "error": "Score not found"
            }), 404
            
        return jsonify({
            "success": True,
            "message": "Score deleted successfully"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to delete score",
            "message": str(e)
        }), 500


@score_api.route("/bulk", methods=["POST"])
@token_required
def create_bulk_scores():
    """Create multiple scores for a round"""
    try:
        # Validate request data
        data = bulk_score_schema.load(request.json)
        
        # Create scores via service
        scores = ScoreService.create_scores_for_holes(
            data['round_id'], 
            data['hole_scores']
        )
        
        return jsonify({
            "success": True,
            "data": scores,
            "count": len(scores),
            "message": "Scores created successfully"
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
            "error": "Failed to create scores",
            "message": str(e)
        }), 500


@score_api.route("/round/<int:round_id>/recalculate", methods=["POST"])
@token_required
def recalculate_round_points(round_id):
    """Recalculate Stableford points for all scores in a round"""
    try:
        round_data = ScoreService.recalculate_round_points(round_id)
        
        return jsonify({
            "success": True,
            "data": round_data,
            "message": "Points recalculated successfully"
        }), 200
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to recalculate points",
            "message": str(e)
        }), 500 