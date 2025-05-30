"""
Course API Routes

Thin routes that handle HTTP concerns only.
All business logic is delegated to CourseService.
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.services.course_service import CourseService
from app.services.auth_service import admin_required, token_required
from app.schemas.course_schema import (
    CourseCreateSchema, CourseUpdateSchema, CourseResponseSchema,
    CourseSearchSchema, DefaultTeeSetSchema
)

course_api = Blueprint('course_api', __name__)

# Initialize schemas
course_create_schema = CourseCreateSchema()
course_update_schema = CourseUpdateSchema()
course_response_schema = CourseResponseSchema()
course_search_schema = CourseSearchSchema()
default_tee_set_schema = DefaultTeeSetSchema()


@course_api.route("", methods=["GET"])
@token_required
def list_courses():
    """Get all courses with optional filtering"""
    try:
        # Parse query parameters
        club_id = request.args.get('club_id', type=int)
        search = request.args.get('search')
        
        if club_id:
            # Get courses for specific club
            courses = CourseService.get_courses_by_club(club_id)
        elif search:
            # Search courses
            courses = CourseService.search_courses(search)
        else:
            # Get all courses
            courses = CourseService.get_all_courses()
            
        return jsonify({
            "success": True,
            "data": courses,
            "count": len(courses)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve courses",
            "message": str(e)
        }), 500


@course_api.route("/<int:course_id>", methods=["GET"])
@token_required
def get_course(course_id):
    """Get a specific course with optional details"""
    try:
        # Parse query parameters
        include_holes = request.args.get('include_holes', 'false').lower() == 'true'
        include_tee_sets = request.args.get('include_tee_sets', 'false').lower() == 'true'
        full_details = request.args.get('full_details', 'false').lower() == 'true'
        
        if full_details:
            # Get course with complete details including club info
            course = CourseService.get_course_with_full_details(course_id)
        else:
            # Get course with optional includes
            course = CourseService.get_course_by_id(course_id, include_holes, include_tee_sets)
            
        if not course:
            return jsonify({
                "success": False,
                "error": "Course not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": course
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve course",
            "message": str(e)
        }), 500


@course_api.route("", methods=["POST"])
@admin_required
def create_course():
    """Create a new course (admin only)"""
    try:
        # Validate request data
        course_data = course_create_schema.load(request.json)
        
        # Create course via service
        course = CourseService.create_course(course_data)
        
        return jsonify({
            "success": True,
            "data": course,
            "message": "Course created successfully"
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
            "error": "Failed to create course",
            "message": str(e)
        }), 500


@course_api.route("/<int:course_id>", methods=["PUT"])
@admin_required
def update_course(course_id):
    """Update an existing course (admin only)"""
    try:
        # Validate request data
        course_data = course_update_schema.load(request.json)
        
        # Update course via service
        course = CourseService.update_course(course_id, course_data)
        
        if not course:
            return jsonify({
                "success": False,
                "error": "Course not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": course,
            "message": "Course updated successfully"
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
            "error": "Failed to update course",
            "message": str(e)
        }), 500


@course_api.route("/<int:course_id>", methods=["DELETE"])
@admin_required
def delete_course(course_id):
    """Delete a course (admin only)"""
    try:
        success = CourseService.delete_course(course_id)
        
        if not success:
            return jsonify({
                "success": False,
                "error": "Course not found"
            }), 404
            
        return jsonify({
            "success": True,
            "message": "Course deleted successfully"
        }), 200
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to delete course",
            "message": str(e)
        }), 500


@course_api.route("/<int:course_id>/default-tee-set", methods=["PUT"])
@admin_required
def set_default_tee_set(course_id):
    """Set the default tee set for a course (admin only)"""
    try:
        # Validate request data
        data = default_tee_set_schema.load(request.json)
        
        # Set default tee set via service
        course = CourseService.set_default_tee_set(course_id, data['tee_set_id'])
        
        if not course:
            return jsonify({
                "success": False,
                "error": "Course not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": course,
            "message": "Default tee set updated successfully"
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
            "error": "Failed to set default tee set",
            "message": str(e)
        }), 500


@course_api.route("/search", methods=["GET"])
@token_required
def search_courses():
    """Search courses by name or club name"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({
                "success": False,
                "error": "Search query is required"
            }), 400
            
        courses = CourseService.search_courses(query)
        
        return jsonify({
            "success": True,
            "data": courses,
            "count": len(courses),
            "query": query
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to search courses",
            "message": str(e)
        }), 500 