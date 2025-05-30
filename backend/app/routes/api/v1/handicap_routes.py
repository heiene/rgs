"""
Handicap API Routes

Routes for handicap management.
- Admin routes: Can manage all users' handicaps
- User routes: Can only manage their own handicap
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.services.handicap_service import HandicapService
from app.services.user_service import UserService
from app.services.auth_service import token_required, admin_required
from app.schemas.handicap_schema import (
    HandicapCreateSchema, HandicapUpdateSchema, HandicapResponseSchema,
    InitialHandicapSchema
)

handicap_bp = Blueprint('handicaps', __name__)

# Initialize schemas
handicap_create_schema = HandicapCreateSchema()
handicap_update_schema = HandicapUpdateSchema()
handicap_response_schema = HandicapResponseSchema()
initial_handicap_schema = InitialHandicapSchema()


# Admin Routes - Can manage all users' handicaps
@handicap_bp.route('/admin/users/<int:user_id>/handicaps', methods=['GET'])
@admin_required
def admin_get_user_handicaps(user_id):
    """Get handicap history for any user (admin only)"""
    try:
        handicaps = HandicapService.get_user_handicap_history(user_id)
        
        return jsonify({
            'success': True,
            'data': handicaps,
            'count': len(handicaps)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve handicaps',
            'message': str(e)
        }), 500


@handicap_bp.route('/admin/users/<int:user_id>/handicaps', methods=['POST'])
@admin_required
def admin_create_user_handicap(user_id):
    """Create handicap for any user (admin only)"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Validate request data
        handicap_data = handicap_create_schema.load(request.json)
        
        # Ensure user_id matches URL parameter
        handicap_data['user_id'] = user_id
        handicap_data['created_by_id'] = current_user_id
        
        # Create handicap via service
        handicap = HandicapService.create_handicap(handicap_data, current_user_id)
        
        return jsonify({
            'success': True,
            'data': handicap,
            'message': 'Handicap created successfully'
        }), 201
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'Validation failed',
            'details': e.messages
        }), 400
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to create handicap',
            'message': str(e)
        }), 500


@handicap_bp.route('/admin/users/<int:user_id>/handicaps/current', methods=['GET'])
@admin_required
def admin_get_user_current_handicap(user_id):
    """Get current handicap for any user (admin only)"""
    try:
        handicap = HandicapService.get_current_handicap(user_id)
        
        if not handicap:
            return jsonify({
                'success': False,
                'error': 'No current handicap found for user'
            }), 404
        
        return jsonify({
            'success': True,
            'data': handicap
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve current handicap',
            'message': str(e)
        }), 500


@handicap_bp.route('/admin/users/<int:user_id>/handicaps/initial', methods=['POST'])
@admin_required
def admin_set_initial_handicap(user_id):
    """Set initial handicap for any user (admin only)"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Validate request data
        handicap_data = initial_handicap_schema.load(request.json)
        
        # Ensure user_id matches URL parameter
        handicap_data['user_id'] = user_id
        
        # Set initial handicap via service
        handicap = HandicapService.set_initial_handicap(
            user_id, 
            handicap_data['handicap_value'], 
            current_user_id
        )
        
        return jsonify({
            'success': True,
            'data': handicap,
            'message': 'Initial handicap set successfully'
        }), 201
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'Validation failed',
            'details': e.messages
        }), 400
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to set initial handicap',
            'message': str(e)
        }), 500


@handicap_bp.route('/admin/handicaps/<int:handicap_id>', methods=['PUT'])
@admin_required
def admin_update_handicap(handicap_id):
    """Update any handicap (admin only)"""
    try:
        # Validate request data
        handicap_data = handicap_update_schema.load(request.json)
        
        # Update handicap via service
        updated_handicap = HandicapService.update_handicap(handicap_id, handicap_data)
        
        if not updated_handicap:
            return jsonify({
                'success': False,
                'error': 'Handicap not found'
            }), 404
            
        return jsonify({
            'success': True,
            'data': updated_handicap,
            'message': 'Handicap updated successfully'
        }), 200
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'Validation failed',
            'details': e.messages
        }), 400
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to update handicap',
            'message': str(e)
        }), 500


@handicap_bp.route('/admin/handicaps/<int:handicap_id>', methods=['DELETE'])
@admin_required
def admin_delete_handicap(handicap_id):
    """Delete any handicap (admin only)"""
    try:
        success = HandicapService.delete_handicap(handicap_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Handicap not found'
            }), 404
            
        return jsonify({
            'success': True,
            'message': 'Handicap deleted successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to delete handicap',
            'message': str(e)
        }), 500


# User Routes - Can only manage their own handicap
@handicap_bp.route('/my-handicaps', methods=['GET'])
@token_required
def get_my_handicaps():
    """Get current user's handicap history"""
    try:
        current_user_id = int(get_jwt_identity())
        handicaps = HandicapService.get_user_handicap_history(current_user_id)
        
        return jsonify({
            'success': True,
            'data': handicaps,
            'count': len(handicaps)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve handicaps',
            'message': str(e)
        }), 500


@handicap_bp.route('/my-handicaps/current', methods=['GET'])
@token_required
def get_my_current_handicap():
    """Get current user's current handicap"""
    try:
        current_user_id = int(get_jwt_identity())
        handicap = HandicapService.get_current_handicap(current_user_id)
        
        if not handicap:
            return jsonify({
                'success': False,
                'error': 'No current handicap found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': handicap
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve current handicap',
            'message': str(e)
        }), 500


@handicap_bp.route('/my-handicaps', methods=['POST'])
@token_required
def update_my_handicap():
    """Update current user's handicap"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Validate request data
        handicap_data = handicap_create_schema.load(request.json)
        
        # Ensure user can only update their own handicap
        handicap_data['user_id'] = current_user_id
        handicap_data['created_by_id'] = current_user_id
        
        # Create new handicap entry (self-reported)
        handicap = HandicapService.create_handicap(handicap_data, current_user_id)
        
        return jsonify({
            'success': True,
            'data': handicap,
            'message': 'Handicap updated successfully'
        }), 201
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'Validation failed',
            'details': e.messages
        }), 400
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to update handicap',
            'message': str(e)
        }), 500


@handicap_bp.route('/my-handicaps/initial', methods=['POST'])
@token_required
def set_my_initial_handicap():
    """Set current user's initial handicap"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Validate request data
        handicap_data = initial_handicap_schema.load(request.json)
        
        # Set initial handicap via service
        handicap = HandicapService.set_initial_handicap(
            current_user_id, 
            handicap_data['handicap_value'], 
            current_user_id
        )
        
        return jsonify({
            'success': True,
            'data': handicap,
            'message': 'Initial handicap set successfully'
        }), 201
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'Validation failed',
            'details': e.messages
        }), 400
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to set initial handicap',
            'message': str(e)
        }), 500 