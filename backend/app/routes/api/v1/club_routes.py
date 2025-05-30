"""
Club API Routes

Thin routes that handle HTTP concerns only.
All business logic is delegated to ClubService.
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.services.club_service import ClubService
from app.services.auth_service import admin_required, token_required
from app.schemas.club_schema import (
    ClubCreateSchema, ClubUpdateSchema, ClubResponseSchema, 
    ClubWithCoursesSchema, ClubSearchSchema
)

club_api = Blueprint('club_api', __name__)

# Initialize schemas
club_create_schema = ClubCreateSchema()
club_update_schema = ClubUpdateSchema()
club_response_schema = ClubResponseSchema()
club_with_courses_schema = ClubWithCoursesSchema()
club_search_schema = ClubSearchSchema()


@club_api.route("", methods=["GET"])
@token_required
def list_clubs():
    """Get all clubs - requires authentication"""
    try:
        # Check for search parameters
        search_query = request.args.get('search')
        country = request.args.get('country')
        
        if search_query:
            clubs = ClubService.search_clubs(search_query)
        elif country:
            clubs = ClubService.get_clubs_by_country(country)
        else:
            clubs = ClubService.get_all_clubs()
            
        return jsonify({
            "success": True,
            "data": clubs,
            "count": len(clubs)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve clubs",
            "message": str(e)
        }), 500


@club_api.route("/<int:club_id>", methods=["GET"])
@token_required
def get_club(club_id):
    """Get a specific club - requires authentication"""
    try:
        # Check if courses should be included
        include_courses = request.args.get('include_courses', 'false').lower() == 'true'
        
        if include_courses:
            club = ClubService.get_club_with_courses(club_id)
        else:
            club = ClubService.get_club_by_id(club_id)
            
        if not club:
            return jsonify({
                "success": False,
                "error": "Club not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": club
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve club",
            "message": str(e)
        }), 500


@club_api.route("", methods=["POST"])
@admin_required
def create_club():
    """Create a new club (admin only)"""
    try:
        # Validate request data
        club_data = club_create_schema.load(request.json)
        
        # Create club via service
        club = ClubService.create_club(club_data)
        
        return jsonify({
            "success": True,
            "data": club,
            "message": "Club created successfully"
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
            "error": "Failed to create club",
            "message": str(e)
        }), 500


@club_api.route("/<int:club_id>", methods=["PUT"])
@admin_required
def update_club(club_id):
    """Update an existing club (admin only)"""
    try:
        # Validate request data
        club_data = club_update_schema.load(request.json)
        
        # Update club via service
        club = ClubService.update_club(club_id, club_data)
        
        if not club:
            return jsonify({
                "success": False,
                "error": "Club not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": club,
            "message": "Club updated successfully"
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
            "error": "Failed to update club",
            "message": str(e)
        }), 500


@club_api.route("/<int:club_id>", methods=["DELETE"])
@admin_required
def delete_club(club_id):
    """Delete a club (admin only)"""
    try:
        success = ClubService.delete_club(club_id)
        
        if not success:
            return jsonify({
                "success": False,
                "error": "Club not found"
            }), 404
            
        return jsonify({
            "success": True,
            "message": "Club deleted successfully"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to delete club",
            "message": str(e)
        }), 500


@club_api.route("/<int:club_id>/courses", methods=["POST"])
@admin_required
def add_course_to_club(club_id):
    """Add a course to a club (admin only)"""
    try:
        # This will delegate to CourseService
        course = ClubService.add_course_to_club(club_id, request.json)
        
        if not course:
            return jsonify({
                "success": False,
                "error": "Club not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": course,
            "message": "Course added to club successfully"
        }), 201
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to add course to club",
            "message": str(e)
        }), 500