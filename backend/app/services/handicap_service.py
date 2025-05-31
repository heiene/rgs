"""
Handicap Service

Contains all business logic for handicap operations including temporal data management.
Follows the "Fat Services, Thin Routes" pattern.
"""
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models.handicap import Handicap
from app.models.user import User


class HandicapService:
    """Service class for handicap business logic with temporal data management"""

    @staticmethod
    def get_user_handicap_history(user_id: int) -> List[Dict[str, Any]]:
        """
        Get complete handicap history for a user.
        
        Args:
            user_id: The user ID
            
        Returns:
            List of handicap dictionaries ordered by start_date
        """
        handicaps = Handicap.query.filter_by(user_id=user_id).order_by(Handicap.start_date.desc()).all()
        return [handicap.to_dict() for handicap in handicaps]

    @staticmethod
    def get_current_handicap(user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user's current handicap.
        
        Args:
            user_id: The user ID
            
        Returns:
            Current handicap dictionary or None if not found
        """
        handicap = Handicap.query.filter_by(user_id=user_id, end_date=None).first()
        return handicap.to_dict() if handicap else None

    @staticmethod
    def get_handicap_on_date(user_id: int, check_date: date = None) -> Optional[Dict[str, Any]]:
        """
        Get user's handicap that was valid on a specific date.
        
        Args:
            user_id: The user ID
            check_date: Date to check (defaults to today)
            
        Returns:
            Handicap dictionary or None if not found
        """
        if check_date is None:
            check_date = date.today()
            
        handicap = Handicap.get_handicap_on_date(user_id, check_date)
        return handicap.to_dict() if handicap else None

    @staticmethod
    def create_handicap(handicap_data: Dict[str, Any], created_by_id: int) -> Dict[str, Any]:
        """
        Create a new handicap with temporal logic.
        This handles the complex logic you described for fitting handicaps into history.
        
        Args:
            handicap_data: Dictionary containing handicap information
            created_by_id: ID of user creating the handicap
            
        Returns:
            Created handicap dictionary
            
        Raises:
            ValueError: If handicap data is invalid
        """
        # Validate required fields
        required_fields = ['user_id', 'handicap_value', 'start_date']
        for field in required_fields:
            if field not in handicap_data:
                raise ValueError(f"{field} is required")
        
        user_id = handicap_data['user_id']
        new_value = handicap_data['handicap_value']
        new_start_date = handicap_data['start_date']
        
        if isinstance(new_start_date, str):
            new_start_date = datetime.strptime(new_start_date, '%Y-%m-%d').date()
        
        # Verify user exists
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Get the user who is creating this handicap for auto-generation of reason
        created_by_user = User.query.get(created_by_id)
        if not created_by_user:
            raise ValueError("Created by user not found")
        
        # Auto-generate reason if not provided or empty
        reason = handicap_data.get('reason', '').strip()
        if not reason:
            # Check if this is the user's first handicap
            existing_handicaps = Handicap.query.filter_by(user_id=user_id).count()
            if existing_handicaps == 0:
                reason = f"Initial handicap set by {created_by_user.full_name}"
            else:
                reason = f"Handicap updated by {created_by_user.full_name}"

        try:
            # Handle temporal logic for inserting handicap into history
            HandicapService._insert_handicap_into_timeline(
                user_id, new_value, new_start_date, created_by_id, reason
            )
            
            # Return the current handicap (the one active today) rather than the newly created one
            # This is important because with temporal logic, the newly created handicap might not be current
            current_handicap = HandicapService.get_current_handicap(user_id)
            if current_handicap:
                return current_handicap
            else:
                # Fallback to the newly created handicap if no current one found
                new_handicap = Handicap.query.filter_by(
                    user_id=user_id, 
                    start_date=new_start_date,
                    handicap_value=new_value
                ).first()
                return new_handicap.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Failed to create handicap due to database constraints")

    @staticmethod
    def _insert_handicap_into_timeline(user_id: int, value: float, start_date: date, created_by_id: int, reason: str):
        """
        Complex temporal logic for inserting a handicap into the timeline.
        
        This implements your requirement:
        - If hcp 10 is valid from 1st Jan 2024, and new hcp 11 is entered on 1st Jan 2025
        - When hcp 12 is entered on 1st June 2024, the 10 hcp gets end_date of 1st June
        - The 12 hcp runs from 1st June to 1st Jan 2025, then 11 hcp takes over
        """
        
        # Find all existing handicaps for this user
        existing_handicaps = Handicap.query.filter_by(user_id=user_id).order_by(Handicap.start_date).all()
        
        # Find handicap that should end when this one starts
        handicap_to_end = None
        handicap_to_adjust = None
        
        for hcp in existing_handicaps:
            # If this handicap starts before or on the new start date
            if hcp.start_date <= start_date:
                # And either has no end date or ends after the new start date
                if hcp.end_date is None or hcp.end_date > start_date:
                    handicap_to_end = hcp
            
            # If this handicap starts after the new start date, it might need adjustment
            elif hcp.start_date > start_date:
                if handicap_to_adjust is None:
                    handicap_to_adjust = hcp
                break
        
        # Create the new handicap
        new_handicap = Handicap(
            user_id=user_id,
            handicap_value=value,
            start_date=start_date,
            end_date=handicap_to_adjust.start_date if handicap_to_adjust else None,
            reason=reason,
            created_by_id=created_by_id
        )
        
        # If there's a handicap to end, set its end date
        if handicap_to_end:
            # Only set end date if it's currently None (current handicap) or if the new date is earlier
            if handicap_to_end.end_date is None:
                handicap_to_end.end_date = start_date
            elif start_date < handicap_to_end.end_date:
                handicap_to_end.end_date = start_date
        
        db.session.add(new_handicap)
        db.session.commit()

    @staticmethod
    def update_handicap(handicap_id: int, handicap_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing handicap.
        
        Args:
            handicap_id: The handicap ID
            handicap_data: Dictionary containing updated handicap information
            
        Returns:
            Updated handicap dictionary or None if not found
        """
        handicap = Handicap.query.get(handicap_id)
        if not handicap:
            return None

        # Update simple fields only (temporal logic changes require new entries)
        if 'handicap_value' in handicap_data:
            handicap.handicap_value = handicap_data['handicap_value']
        
        if 'reason' in handicap_data:
            handicap.reason = handicap_data['reason']

        db.session.commit()
        return handicap.to_dict()

    @staticmethod
    def delete_handicap(handicap_id: int) -> bool:
        """
        Delete a handicap entry.
        
        Args:
            handicap_id: The handicap ID
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            ValueError: If trying to delete the only handicap
        """
        handicap = Handicap.query.get(handicap_id)
        if not handicap:
            return False

        # Check if this is the user's only handicap
        user_handicap_count = Handicap.query.filter_by(user_id=handicap.user_id).count()
        if user_handicap_count <= 1:
            raise ValueError("Cannot delete user's only handicap entry")

        db.session.delete(handicap)
        db.session.commit()
        return True

    @staticmethod
    def calculate_handicap_differential(gross_score: int, course_rating: float, slope_rating: float) -> float:
        """
        Calculate handicap differential for a round.
        
        Args:
            gross_score: Total strokes for the round
            course_rating: Course rating for the tees played
            slope_rating: Slope rating for the tees played
            
        Returns:
            Handicap differential
        """
        return round((gross_score - course_rating) * 113 / slope_rating, 1) 