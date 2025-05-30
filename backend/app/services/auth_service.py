"""
Authentication Service

Contains authentication and authorization logic.
Provides decorators for protecting routes.
"""
from flask import request, jsonify, current_app
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
import jwt


def token_required(f):
    """
    Decorator to require valid JWT token for route access.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({
                "success": False,
                "error": "Authentication required",
                "message": "Valid token required"
            }), 401
    return decorated_function


def admin_required(f):
    """
    Decorator to require admin privileges for route access.
    Checks both authentication and admin role.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # First verify JWT token
            verify_jwt_in_request()
            
            # Get user identity from token
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            
            # Check if user has admin role
            # TODO: Replace with actual admin check when User model is implemented
            user_is_admin = claims.get('is_admin', False)
            
            if not user_is_admin:
                return jsonify({
                    "success": False,
                    "error": "Admin access required",
                    "message": "Insufficient privileges"
                }), 403
                
            return f(*args, **kwargs)
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": "Authentication required",
                "message": "Valid admin token required"
            }), 401
    return decorated_function


def optional_auth(f):
    """
    Decorator for routes that work with or without authentication.
    Sets current_user to None if no valid token.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)
        except Exception:
            pass  # Continue without authentication
        return f(*args, **kwargs)
    return decorated_function


class AuthService:
    """Service class for authentication business logic"""
    
    @staticmethod
    def verify_admin_token(token: str) -> bool:
        """
        Verify if a token belongs to an admin user.
        
        Args:
            token: JWT token string
            
        Returns:
            True if token is valid and belongs to admin
        """
        try:
            payload = jwt.decode(
                token, 
                current_app.config['JWT_SECRET_KEY'], 
                algorithms=['HS256']
            )
            return payload.get('is_admin', False)
        except jwt.InvalidTokenError:
            return False
    
    @staticmethod
    def get_current_user_id() -> int:
        """
        Get current authenticated user ID from JWT token.
        
        Returns:
            User ID or None if not authenticated
        """
        try:
            return get_jwt_identity()
        except Exception:
            return None
    
    @staticmethod
    def is_current_user_admin() -> bool:
        """
        Check if current authenticated user is admin.
        
        Returns:
            True if current user is admin
        """
        try:
            claims = get_jwt()
            return claims.get('is_admin', False)
        except Exception:
            return False