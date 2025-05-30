"""
TeeSet Service

Contains all business logic for tee set operations.
Follows the "Fat Services, Thin Routes" pattern.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models.tee_set import TeeSet
from app.models.course import Course


class TeeSetService:
    """Service class for tee set business logic"""

    @staticmethod
    def get_tee_sets_by_course(course_id: int, include_positions: bool = False) -> List[Dict[str, Any]]:
        """
        Get all tee sets for a specific course.
        
        Args:
            course_id: The course ID
            include_positions: Whether to include tee position data
            
        Returns:
            List of tee set dictionaries
        """
        tee_sets = TeeSet.query.filter_by(course_id=course_id).all()
        return [tee_set.to_dict(include_positions=include_positions) for tee_set in tee_sets]

    @staticmethod
    def get_tee_set_by_id(tee_set_id: int, include_positions: bool = False) -> Optional[Dict[str, Any]]:
        """
        Get a specific tee set by ID.
        
        Args:
            tee_set_id: The tee set ID
            include_positions: Whether to include tee position data
            
        Returns:
            Tee set dictionary or None if not found
        """
        tee_set = TeeSet.query.get(tee_set_id)
        return tee_set.to_dict(include_positions=include_positions) if tee_set else None

    @staticmethod
    def create_tee_set(tee_set_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new tee set.
        
        Args:
            tee_set_data: Dictionary containing tee set information
            
        Returns:
            Created tee set dictionary
            
        Raises:
            ValueError: If tee set data is invalid
        """
        # Validate required fields
        required_fields = ['name', 'slope_rating', 'course_rating', 'course_id']
        for field in required_fields:
            if field not in tee_set_data:
                raise ValueError(f"{field} is required")
        
        # Verify course exists
        course = Course.query.get(tee_set_data['course_id'])
        if not course:
            raise ValueError("Course not found")
        
        # Validate slope rating (typically 55-155)
        slope_rating = tee_set_data['slope_rating']
        if slope_rating < 55 or slope_rating > 155:
            raise ValueError("Slope rating must be between 55 and 155")
        
        # Validate course rating (typically between 60-80 for most courses)
        course_rating = tee_set_data['course_rating']
        if course_rating < 50 or course_rating > 90:
            raise ValueError("Course rating must be between 50 and 90")
        
        # Validate women's ratings if provided
        women_slope = tee_set_data.get('women_slope_rating')
        women_course = tee_set_data.get('women_course_rating')
        
        if women_slope is not None:
            if women_slope < 55 or women_slope > 155:
                raise ValueError("Women's slope rating must be between 55 and 155")
                
        if women_course is not None:
            if women_course < 50 or women_course > 90:
                raise ValueError("Women's course rating must be between 50 and 90")

        try:
            tee_set = TeeSet(
                name=tee_set_data['name'],
                slope_rating=slope_rating,
                course_rating=course_rating,
                women_slope_rating=women_slope,
                women_course_rating=women_course,
                course_id=tee_set_data['course_id']
            )
            
            db.session.add(tee_set)
            db.session.commit()
            
            return tee_set.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Failed to create tee set due to database constraints")

    @staticmethod
    def update_tee_set(tee_set_id: int, tee_set_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing tee set.
        
        Args:
            tee_set_id: The tee set ID
            tee_set_data: Dictionary containing updated tee set information
            
        Returns:
            Updated tee set dictionary or None if not found
            
        Raises:
            ValueError: If tee set data is invalid
        """
        tee_set = TeeSet.query.get(tee_set_id)
        if not tee_set:
            return None

        try:
            # Update fields if provided
            if 'name' in tee_set_data:
                if not tee_set_data['name']:
                    raise ValueError("Tee set name cannot be empty")
                tee_set.name = tee_set_data['name']
            
            if 'slope_rating' in tee_set_data:
                slope_rating = tee_set_data['slope_rating']
                if slope_rating < 55 or slope_rating > 155:
                    raise ValueError("Slope rating must be between 55 and 155")
                tee_set.slope_rating = slope_rating
            
            if 'course_rating' in tee_set_data:
                course_rating = tee_set_data['course_rating']
                if course_rating < 50 or course_rating > 90:
                    raise ValueError("Course rating must be between 50 and 90")
                tee_set.course_rating = course_rating
            
            if 'women_slope_rating' in tee_set_data:
                women_slope = tee_set_data['women_slope_rating']
                if women_slope is not None and (women_slope < 55 or women_slope > 155):
                    raise ValueError("Women's slope rating must be between 55 and 155")
                tee_set.women_slope_rating = women_slope
            
            if 'women_course_rating' in tee_set_data:
                women_course = tee_set_data['women_course_rating']
                if women_course is not None and (women_course < 50 or women_course > 90):
                    raise ValueError("Women's course rating must be between 50 and 90")
                tee_set.women_course_rating = women_course

            db.session.commit()
            return tee_set.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Failed to update tee set due to database constraints")

    @staticmethod
    def delete_tee_set(tee_set_id: int) -> bool:
        """
        Delete a tee set.
        
        Args:
            tee_set_id: The tee set ID
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            ValueError: If tee set has associated rounds or is default for course
        """
        tee_set = TeeSet.query.get(tee_set_id)
        if not tee_set:
            return False

        # Check if tee set has rounds
        if tee_set.rounds:
            raise ValueError(f"Cannot delete tee set '{tee_set.name}' - it has {len(tee_set.rounds)} associated round(s)")
        
        # Check if it's the default tee set for the course
        if tee_set.course and tee_set.course.default_tee_set_id == tee_set_id:
            raise ValueError(f"Cannot delete tee set '{tee_set.name}' - it is the default tee set for the course")

        db.session.delete(tee_set)
        db.session.commit()
        return True

    @staticmethod
    def get_rating_for_gender(tee_set_id: int, gender: str = 'M') -> Optional[Dict[str, float]]:
        """
        Get course and slope rating for specific gender.
        
        Args:
            tee_set_id: The tee set ID
            gender: Gender ('M' for men, 'F' for women)
            
        Returns:
            Dictionary with course_rating and slope_rating or None if not found
        """
        tee_set = TeeSet.query.get(tee_set_id)
        if not tee_set:
            return None
            
        return tee_set.get_rating_for_gender(gender)

    @staticmethod
    def create_standard_tee_sets(course_id: int) -> List[Dict[str, Any]]:
        """
        Create standard tee sets for a course.
        
        Args:
            course_id: The course ID
            
        Returns:
            List of created tee set dictionaries
            
        Raises:
            ValueError: If course not found or already has tee sets
        """
        # Verify course exists
        course = Course.query.get(course_id)
        if not course:
            raise ValueError("Course not found")
        
        # Check if course already has tee sets
        existing_tee_sets = TeeSet.query.filter_by(course_id=course_id).count()
        if existing_tee_sets > 0:
            raise ValueError("Course already has tee sets")
        
        # Standard tee set configurations
        standard_tee_sets = [
            {
                'name': 'Championship',
                'slope_rating': 130,
                'course_rating': 74.2,
                'women_slope_rating': 125,
                'women_course_rating': 70.8
            },
            {
                'name': 'Yellow',
                'slope_rating': 125,
                'course_rating': 72.1,
                'women_slope_rating': 120,
                'women_course_rating': 69.2
            },
            {
                'name': 'Red',
                'slope_rating': 115,
                'course_rating': 68.5,
                'women_slope_rating': 110,
                'women_course_rating': 66.1
            }
        ]
        
        created_tee_sets = []
        
        try:
            for tee_data in standard_tee_sets:
                tee_data['course_id'] = course_id
                tee_set = TeeSetService.create_tee_set(tee_data)
                created_tee_sets.append(tee_set)
            
            return created_tee_sets
            
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to create standard tee sets: {str(e)}")

    @staticmethod
    def get_tee_set_statistics(tee_set_id: int) -> Optional[Dict[str, Any]]:
        """
        Get statistics for a specific tee set.
        
        Args:
            tee_set_id: The tee set ID
            
        Returns:
            Dictionary with tee set statistics
        """
        tee_set = TeeSet.query.get(tee_set_id)
        if not tee_set:
            return None
        
        # Basic tee set info
        stats = tee_set.to_dict(include_positions=True)
        
        # Add usage statistics
        stats['usage_stats'] = {
            'total_rounds': len(tee_set.rounds),
            'total_length_meters': tee_set.total_length_meters,
            'total_length_yards': round(tee_set.total_length_meters * 1.09361) if tee_set.total_length_meters else None,
            'is_default': tee_set.course.default_tee_set_id == tee_set_id if tee_set.course else False,
            'has_women_ratings': bool(tee_set.women_course_rating and tee_set.women_slope_rating)
        }
        
        return stats

    @staticmethod
    def validate_tee_set_setup(course_id: int) -> Dict[str, Any]:
        """
        Validate tee set setup for a course.
        
        Args:
            course_id: The course ID
            
        Returns:
            Dictionary with validation results
        """
        course = Course.query.get(course_id)
        if not course:
            return {"valid": False, "error": "Course not found"}
        
        tee_sets = TeeSet.query.filter_by(course_id=course_id).all()
        
        validation = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "tee_set_count": len(tee_sets)
        }
        
        if not tee_sets:
            validation["valid"] = False
            validation["errors"].append("Course has no tee sets")
            return validation
        
        # Check if course has a default tee set
        if not course.default_tee_set_id:
            validation["warnings"].append("Course has no default tee set")
        
        # Check if tee sets have proper hole coverage
        holes_count = len(course.holes)
        for tee_set in tee_sets:
            positions_count = len(tee_set.tee_positions)
            if positions_count != holes_count:
                validation["warnings"].append(f"Tee set '{tee_set.name}' has {positions_count} positions but course has {holes_count} holes")
        
        # Check rating ranges
        for tee_set in tee_sets:
            if tee_set.slope_rating < 100 or tee_set.slope_rating > 140:
                validation["warnings"].append(f"Tee set '{tee_set.name}' has unusual slope rating: {tee_set.slope_rating}")
        
        return validation 