"""
Authentication API routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from marshmallow import Schema, fields, ValidationError, validate
from app.models.user import User
from app.services.user_service import UserService
from app.services.email_service import EmailService
from app.extensions import db

auth_bp = Blueprint('auth', __name__)


# Schemas for validation
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    sex = fields.Str(validate=validate.OneOf(['M', 'F']), missing='M')


class PasswordResetRequestSchema(Schema):
    email = fields.Email(required=True)


class PasswordResetSchema(Schema):
    token = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=validate.Length(min=8))


# Initialize schemas
login_schema = LoginSchema()
register_schema = RegisterSchema()
password_reset_request_schema = PasswordResetRequestSchema()
password_reset_schema = PasswordResetSchema()


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        # Validate request data
        data = login_schema.load(request.json)
        
        # Find user by email
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({
                'success': False,
                'error': 'Invalid credentials'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Account is deactivated'
            }), 401
        
        # Update last login
        UserService.update_last_login(user.id)
        
        # Create tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'success': True,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
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
            'error': 'Login failed',
            'message': str(e)
        }), 500


@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        # Validate request data
        data = register_schema.load(request.json)
        
        # Create user via service
        user = UserService.create_user(data)
        
        # Send welcome email
        user_obj = User.query.get(user['id'])
        EmailService.send_welcome_email(user_obj)
        
        # Get user data with admin field for registration response
        user_with_admin = user_obj.to_dict(include_sensitive=True)
        
        # Create access token for immediate login
        access_token = create_access_token(identity=str(user['id']))
        
        return jsonify({
            'success': True,
            'access_token': access_token,
            'user': user_with_admin,
            'message': 'User registered successfully'
        }), 201
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'Validation failed',
            'message': 'Validation failed',
            'details': e.messages
        }), 400
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Registration failed',
            'message': str(e)
        }), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    try:
        current_user_id = get_jwt_identity()
        new_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'success': True,
            'access_token': new_token
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Token refresh failed',
            'message': str(e)
        }), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user info"""
    try:
        current_user_id = int(get_jwt_identity())
        user = UserService.get_user_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get user info',
            'message': str(e)
        }), 500


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Request password reset email"""
    try:
        # Validate request data
        data = password_reset_request_schema.load(request.json)
        
        # Send reset email (always returns success for security)
        EmailService.send_password_reset_email(data['email'])
        
        return jsonify({
            'success': True,
            'message': 'Password reset email sent'
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
            'error': 'Failed to process password reset request',
            'message': str(e)
        }), 500


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password using token"""
    try:
        # Validate request data
        data = password_reset_schema.load(request.json)
        
        # Verify token
        user = EmailService.verify_reset_token(data['token'])
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired reset token',
                'message': 'Invalid or expired token'
            }), 400
        
        # Update password
        user.set_password(data['new_password'])
        
        # Clear reset token
        EmailService.clear_reset_token(user)
        
        # Send confirmation email
        EmailService.send_password_changed_notification(user)
        
        return jsonify({
            'success': True,
            'message': 'Password reset successfully'
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
            'error': 'Failed to reset password',
            'message': str(e)
        }), 500 