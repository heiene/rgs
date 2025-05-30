"""
Club Service

Contains all business logic for club operations.
Follows the "Fat Services, Thin Routes" pattern.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models.club import Club


class ClubService:
    """Service class for club business logic"""

    @staticmethod
    def get_all_clubs() -> List[Dict[str, Any]]:
        """
        Get all clubs with basic information.
        
        Returns:
            List of club dictionaries
        """
        clubs = Club.query.all()
        return [club.to_dict() for club in clubs]

    @staticmethod
    def get_club_by_id(club_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific club by ID.
        
        Args:
            club_id: The club ID
            
        Returns:
            Club dictionary or None if not found
        """
        club = Club.query.get(club_id)
        return club.to_dict() if club else None

    @staticmethod
    def get_club_with_courses(club_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a club with all its courses.
        
        Args:
            club_id: The club ID
            
        Returns:
            Club dictionary with courses or None if not found
        """
        club = Club.query.get(club_id)
        if not club:
            return None
            
        club_data = club.to_dict()
        club_data['courses'] = [course.to_dict() for course in club.courses]
        club_data['course_count'] = len(club.courses)
        return club_data

    @staticmethod
    def create_club(club_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new club.
        
        Args:
            club_data: Dictionary containing club information
            
        Returns:
            Created club dictionary
            
        Raises:
            ValueError: If club data is invalid
            IntegrityError: If club name already exists
        """
        # Validate required fields
        if not club_data.get('name'):
            raise ValueError("Club name is required")

        try:
            club = Club(
                name=club_data['name'],
                description=club_data.get('description'),
                website=club_data.get('website'),
                email=club_data.get('email'),
                phone=club_data.get('phone'),
                address=club_data.get('address'),
                city=club_data.get('city'),
                country=club_data.get('country')
            )
            
            db.session.add(club)
            db.session.commit()
            
            return club.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError(f"Club with name '{club_data['name']}' already exists")

    @staticmethod
    def update_club(club_id: int, club_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing club.
        
        Args:
            club_id: The club ID
            club_data: Dictionary containing updated club information
            
        Returns:
            Updated club dictionary or None if not found
            
        Raises:
            ValueError: If club data is invalid
        """
        club = Club.query.get(club_id)
        if not club:
            return None

        try:
            # Update fields if provided
            if 'name' in club_data:
                if not club_data['name']:
                    raise ValueError("Club name cannot be empty")
                club.name = club_data['name']
            
            if 'description' in club_data:
                club.description = club_data['description']
            if 'website' in club_data:
                club.website = club_data['website']
            if 'email' in club_data:
                club.email = club_data['email']
            if 'phone' in club_data:
                club.phone = club_data['phone']
            if 'address' in club_data:
                club.address = club_data['address']
            if 'city' in club_data:
                club.city = club_data['city']
            if 'country' in club_data:
                club.country = club_data['country']

            db.session.commit()
            return club.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError(f"Club with name '{club_data.get('name')}' already exists")

    @staticmethod
    def delete_club(club_id: int) -> bool:
        """
        Delete a club and all its courses.
        
        Args:
            club_id: The club ID
            
        Returns:
            True if deleted, False if not found
        """
        club = Club.query.get(club_id)
        if not club:
            return False

        db.session.delete(club)
        db.session.commit()
        return True

    @staticmethod
    def search_clubs(query: str) -> List[Dict[str, Any]]:
        """
        Search clubs by name or city.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching club dictionaries
        """
        clubs = Club.query.filter(
            db.or_(
                Club.name.ilike(f'%{query}%'),
                Club.city.ilike(f'%{query}%')
            )
        ).all()
        
        return [club.to_dict() for club in clubs]

    @staticmethod
    def get_clubs_by_country(country: str) -> List[Dict[str, Any]]:
        """
        Get all clubs in a specific country.
        
        Args:
            country: Country name
            
        Returns:
            List of club dictionaries
        """
        clubs = Club.query.filter(Club.country.ilike(f'%{country}%')).all()
        return [club.to_dict() for club in clubs]

    @staticmethod
    def add_course_to_club(club_id: int, course_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Add a new course to a club.
        
        Args:
            club_id: The club ID
            course_data: Dictionary containing course information
            
        Returns:
            Created course dictionary or None if club not found
            
        Raises:
            ValueError: If course data is invalid
        """
        club = Club.query.get(club_id)
        if not club:
            return None

        # Import here to avoid circular imports
        from app.services.course_service import CourseService
        
        course_data['club_id'] = club_id
        return CourseService.create_course(course_data) 