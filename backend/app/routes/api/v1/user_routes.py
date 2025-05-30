"""
User API Routes

Simple routes for user management.
All business logic is delegated to UserService.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.services.user_service import UserService
from app.services.auth_service import token_required, admin_required
from app.schemas.user_schema import (
    UserCreateSchema, UserUpdateSchema, UserPasswordUpdateSchema,
    UserResponseSchema, UserAdminResponseSchema, UserSearchSchema
)

user_bp = Blueprint('users', __name__)

# Initialize schemas
user_create_schema = UserCreateSchema()
user_update_schema = UserUpdateSchema()
user_password_schema = UserPasswordUpdateSchema()
user_response_schema = UserResponseSchema()
user_admin_response_schema = UserAdminResponseSchema()
user_search_schema = UserSearchSchema()


@user_bp.route('/', methods=['GET'])
@admin_required
def get_users():
    """Get all users (admin only)"""
    try:
        # Parse and validate query parameters
        search_params = user_search_schema.load(request.args)
        
        users, meta = UserService.get_all_users(
            page=search_params.get('page', 1),
            per_page=search_params.get('per_page', 20),
            search=search_params.get('search'),
            club_id=search_params.get('club_id'),
            is_active=search_params.get('is_active')
        )
        
        return jsonify({
            'success': True,
            'data': {
                'users': users,
                'meta': meta
            }
        }), 200
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'Validation failed',
            'details': e.messages
        }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve users',
            'message': str(e)
        }), 500


@user_bp.route('/', methods=['POST'])
@admin_required
def create_user():
    """Create a new user (admin only)"""
    try:
        # Validate request data
        user_data = user_create_schema.load(request.json)
        
        # Create user via service
        user = UserService.create_user(user_data)
        
        return jsonify({
            'success': True,
            'data': user,
            'message': 'User created successfully'
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
            'error': 'Failed to create user',
            'message': str(e)
        }), 500


@user_bp.route('/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    """Get a specific user"""
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user is requesting their own data or is admin
        user = UserService.get_user_by_id(current_user_id, include_sensitive=True)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Unauthorized'
            }), 401
        
        is_admin = user.get('is_admin', False)
        is_own_data = current_user_id == user_id
        
        if not (is_admin or is_own_data):
            return jsonify({
                'success': False,
                'error': 'Insufficient permissions'
            }), 403
        
        # Get target user data
        target_user = UserService.get_user_by_id(user_id, include_sensitive=is_admin)
        
        if not target_user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
            
        return jsonify({
            'success': True,
            'data': target_user
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve user',
            'message': str(e)
        }), 500


@user_bp.route('/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    """Update a user"""
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user is updating their own data or is admin
        current_user = UserService.get_user_by_id(current_user_id, include_sensitive=True)
        if not current_user:
            return jsonify({
                'success': False,
                'error': 'Unauthorized'
            }), 401
        
        is_admin = current_user.get('is_admin', False)
        is_own_data = current_user_id == user_id
        
        if not (is_admin or is_own_data):
            return jsonify({
                'success': False,
                'error': 'Insufficient permissions'
            }), 403
        
        # Validate request data
        user_data = user_update_schema.load(request.json)
        
        # Non-admins cannot change is_active status
        if not is_admin and 'is_active' in user_data:
            del user_data['is_active']
        
        # Update user via service
        updated_user = UserService.update_user(user_id, user_data)
        
        if not updated_user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
            
        return jsonify({
            'success': True,
            'data': updated_user,
            'message': 'User updated successfully'
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
            'error': 'Failed to update user',
            'message': str(e)
        }), 500


@user_bp.route('/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete a user (admin only)"""
    try:
        success = UserService.delete_user(user_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
            
        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to delete user',
            'message': str(e)
        }), 500


@user_bp.route('/<int:user_id>/deactivate', methods=['POST'])
@admin_required
def deactivate_user(user_id):
    """Deactivate a user (soft delete, admin only)"""
    try:
        success = UserService.deactivate_user(user_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
            
        return jsonify({
            'success': True,
            'message': 'User deactivated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to deactivate user',
            'message': str(e)
        }), 500


@user_bp.route('/<int:user_id>/password', methods=['PUT'])
@token_required
def update_password(user_id):
    """Update user password"""
    try:
        current_user_id = get_jwt_identity()
        
        # Users can only change their own password
        if current_user_id != user_id:
            return jsonify({
                'success': False,
                'error': 'You can only change your own password'
            }), 403
        
        # Validate request data
        password_data = user_password_schema.load(request.json)
        
        # Update password via service
        UserService.update_user_password(
            user_id,
            password_data['current_password'],
            password_data['new_password']
        )
        
        return jsonify({
            'success': True,
            'message': 'Password updated successfully'
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
            'error': 'Failed to update password',
            'message': str(e)
        }), 500


@user_bp.route('/<int:user_id>/statistics', methods=['GET'])
@token_required
def get_user_statistics(user_id):
    """Get user statistics"""
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user is requesting their own data or is admin
        current_user = UserService.get_user_by_id(current_user_id, include_sensitive=True)
        if not current_user:
            return jsonify({
                'success': False,
                'error': 'Unauthorized'
            }), 401
        
        is_admin = current_user.get('is_admin', False)
        is_own_data = current_user_id == user_id
        
        if not (is_admin or is_own_data):
            return jsonify({
                'success': False,
                'error': 'Insufficient permissions'
            }), 403
        
        # Get statistics via service
        stats = UserService.get_user_statistics(user_id)
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve user statistics',
            'message': str(e)
        }), 500


@user_bp.route('/search', methods=['GET'])
@token_required
def search_users():
    """Search users by name or email"""
    try:
        search_term = request.args.get('q', '').strip()
        limit = min(int(request.args.get('limit', 10)), 50)  # Cap at 50
        
        if not search_term:
            return jsonify({
                'success': False,
                'error': 'Search term is required'
            }), 400
        
        users = UserService.search_users(search_term, limit)
        
        return jsonify({
            'success': True,
            'data': users,
            'count': len(users),
            'search_term': search_term
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to search users',
            'message': str(e)
        }), 500 