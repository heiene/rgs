"""
User Service

Contains all business logic for user operations.
Focused on core user management functionality.
"""
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_
from app.extensions import db
from app.models.user import User
from app.models.club import Club
from app.models.theme import Theme


class UserService:
    """Service class for user business logic"""

    @staticmethod
    def get_all_users(page: int = 1, per_page: int = 20, search: str = None, 
                     club_id: int = None, is_active: bool = None) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Get all users with pagination and filtering"""
        query = User.query
        
        # Apply filters
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    User.email.ilike(search_term),
                    User.first_name.ilike(search_term),
                    User.last_name.ilike(search_term)
                )
            )
        
        if club_id:
            query = query.filter(User.home_club_id == club_id)
            
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        # Apply pagination
        pagination = query.order_by(User.last_name, User.first_name).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        users = [user.to_dict() for user in pagination.items]
        
        meta = {
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next
        }
        
        return users, meta

    @staticmethod
    def get_user_by_id(user_id: int, include_sensitive: bool = False) -> Optional[Dict[str, Any]]:
        """Get a user by ID"""
        user = User.query.get(user_id)
        return user.to_dict(include_sensitive=include_sensitive) if user else None

    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get a user by email"""
        user = User.query.filter_by(email=email).first()
        return user.to_dict() if user else None

    @staticmethod
    def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"{field} is required")
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if existing_user:
            raise ValueError("Email already registered")
        
        # Validate relationships if provided
        if user_data.get('home_club_id'):
            club = Club.query.get(user_data['home_club_id'])
            if not club:
                raise ValueError("Home club not found")
        
        if user_data.get('preferred_theme_id'):
            theme = Theme.query.get(user_data['preferred_theme_id'])
            if not theme:
                raise ValueError("Preferred theme not found")

        try:
            user = User(
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                sex=user_data.get('sex', 'M'),
                distance_unit=user_data.get('distance_unit', 'meters'),
                timezone=user_data.get('timezone', 'Europe/Oslo'),
                country=user_data.get('country'),
                city=user_data.get('city'),
                address=user_data.get('address'),
                postal_code=user_data.get('postal_code'),
                home_club_id=user_data.get('home_club_id'),
                preferred_theme_id=user_data.get('preferred_theme_id'),
                is_admin=user_data.get('is_admin', False)
            )
            
            # Set password
            user.set_password(user_data['password'])
            
            db.session.add(user)
            db.session.commit()
            
            return user.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Failed to create user due to database constraints")

    @staticmethod
    def update_user(user_id: int, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing user"""
        user = User.query.get(user_id)
        if not user:
            return None

        # Validate relationships if provided
        if user_data.get('home_club_id'):
            club = Club.query.get(user_data['home_club_id'])
            if not club:
                raise ValueError("Home club not found")
        
        if user_data.get('preferred_theme_id'):
            theme = Theme.query.get(user_data['preferred_theme_id'])
            if not theme:
                raise ValueError("Preferred theme not found")

        try:
            # Update allowed fields
            updatable_fields = [
                'first_name', 'last_name', 'sex', 'distance_unit', 'timezone',
                'country', 'city', 'address', 'postal_code', 'home_club_id',
                'preferred_theme_id', 'is_active'
            ]
            
            for field in updatable_fields:
                if field in user_data:
                    setattr(user, field, user_data[field])
            
            user.updated_at = datetime.utcnow()
            db.session.commit()
            
            return user.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Failed to update user due to database constraints")

    @staticmethod
    def update_user_password(user_id: int, current_password: str, new_password: str) -> bool:
        """Update user password"""
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Verify current password
        if not user.check_password(current_password):
            raise ValueError("Current password is incorrect")
        
        # Set new password
        user.set_password(new_password)
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        return True

    @staticmethod
    def deactivate_user(user_id: int) -> bool:
        """Deactivate a user (soft delete)"""
        user = User.query.get(user_id)
        if not user:
            return False
        
        user.is_active = False
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return True

    @staticmethod
    def delete_user(user_id: int) -> bool:
        """Delete a user permanently (hard delete)"""
        user = User.query.get(user_id)
        if not user:
            return False

        # Note: Related data (rounds, scores, handicaps) will be deleted due to cascade
        db.session.delete(user)
        db.session.commit()
        return True

    @staticmethod
    def update_last_login(user_id: int) -> None:
        """Update user's last login timestamp"""
        user = User.query.get(user_id)
        if user:
            user.last_login = datetime.utcnow()
            db.session.commit()

    @staticmethod
    def get_users_by_club(club_id: int) -> List[Dict[str, Any]]:
        """Get all users belonging to a specific club"""
        users = User.query.filter_by(home_club_id=club_id, is_active=True).all()
        return [user.to_dict() for user in users]

    @staticmethod
    def search_users(search_term: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search users by name or email"""
        search_pattern = f"%{search_term}%"
        users = User.query.filter(
            and_(
                User.is_active == True,
                or_(
                    User.email.ilike(search_pattern),
                    User.first_name.ilike(search_pattern),
                    User.last_name.ilike(search_pattern)
                )
            )
        ).limit(limit).all()
        
        return [user.to_dict() for user in users]

    @staticmethod
    def get_user_statistics(user_id: int) -> Dict[str, Any]:
        """Get basic statistics for a user"""
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Basic user info
        stats = {
            'user_id': user_id,
            'member_since': user.created_at.isoformat() if user.created_at else None,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'total_rounds': len(user.rounds),
            'current_handicap': user.current_handicap,
            'home_club': user.home_club.name if user.home_club else None
        }
        
        # Calculate completed rounds
        completed_rounds = [r for r in user.rounds if r.is_complete]
        stats['completed_rounds'] = len(completed_rounds)
        
        if completed_rounds:
            # Best score and latest round
            scores = [r.total_score for r in completed_rounds if r.total_score]
            if scores:
                stats['best_score'] = min(scores)
                stats['average_score'] = round(sum(scores) / len(scores), 1)
            
            # Latest differential
            latest_round = max(completed_rounds, key=lambda r: r.date_played)
            stats['latest_differential'] = latest_round.differential
        
        return stats 