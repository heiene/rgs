"""
Course Service

Contains all business logic for course operations.
Follows the "Fat Services, Thin Routes" pattern.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models.course import Course
from app.models.club import Club


class CourseService:
    """Service class for course business logic"""

    @staticmethod
    def get_all_courses() -> List[Dict[str, Any]]:
        """
        Get all courses.
        
        Returns:
            List of course dictionaries
        """
        courses = Course.query.all()
        return [course.to_dict() for course in courses]

    @staticmethod
    def get_course_by_id(course_id: int, include_holes: bool = False, include_tee_sets: bool = False) -> Optional[Dict[str, Any]]:
        """
        Get a specific course by ID.
        
        Args:
            course_id: The course ID
            include_holes: Whether to include hole information
            include_tee_sets: Whether to include tee set information
            
        Returns:
            Course dictionary or None if not found
        """
        course = Course.query.get(course_id)
        return course.to_dict(include_holes=include_holes, include_tee_sets=include_tee_sets) if course else None

    @staticmethod
    def get_courses_by_club(club_id: int) -> List[Dict[str, Any]]:
        """
        Get all courses for a specific club.
        
        Args:
            club_id: The club ID
            
        Returns:
            List of course dictionaries
        """
        courses = Course.query.filter_by(club_id=club_id).all()
        return [course.to_dict() for course in courses]

    @staticmethod
    def create_course(course_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new course.
        
        Args:
            course_data: Dictionary containing course information
            
        Returns:
            Created course dictionary
            
        Raises:
            ValueError: If course data is invalid
        """
        # Validate required fields
        if not course_data.get('name'):
            raise ValueError("Course name is required")
        
        if not course_data.get('club_id'):
            raise ValueError("Club ID is required")
            
        # Verify club exists
        club = Club.query.get(course_data['club_id'])
        if not club:
            raise ValueError("Club not found")

        try:
            course = Course(
                name=course_data['name'],
                holes_count=course_data.get('holes_count', 18),
                description=course_data.get('description'),
                club_id=course_data['club_id'],
                default_tee_set_id=course_data.get('default_tee_set_id')
            )
            
            db.session.add(course)
            db.session.commit()
            
            return course.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Failed to create course due to database constraints")

    @staticmethod
    def update_course(course_id: int, course_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing course.
        
        Args:
            course_id: The course ID
            course_data: Dictionary containing updated course information
            
        Returns:
            Updated course dictionary or None if not found
            
        Raises:
            ValueError: If course data is invalid
        """
        course = Course.query.get(course_id)
        if not course:
            return None

        try:
            # Update fields if provided
            if 'name' in course_data:
                if not course_data['name']:
                    raise ValueError("Course name cannot be empty")
                course.name = course_data['name']
            
            if 'holes_count' in course_data:
                holes_count = course_data['holes_count']
                if holes_count not in [6, 9, 18]:
                    raise ValueError("Holes count must be 6, 9, or 18")
                course.holes_count = holes_count
            
            if 'description' in course_data:
                course.description = course_data['description']
                
            if 'club_id' in course_data:
                # Verify new club exists
                club = Club.query.get(course_data['club_id'])
                if not club:
                    raise ValueError("Club not found")
                course.club_id = course_data['club_id']
                
            if 'default_tee_set_id' in course_data:
                course.default_tee_set_id = course_data['default_tee_set_id']

            db.session.commit()
            return course.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Failed to update course due to database constraints")

    @staticmethod
    def delete_course(course_id: int) -> bool:
        """
        Delete a course and all its holes/tee sets.
        
        Args:
            course_id: The course ID
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            ValueError: If course has associated rounds
        """
        course = Course.query.get(course_id)
        if not course:
            return False

        # Check if course has rounds
        if course.rounds:
            raise ValueError(f"Cannot delete course '{course.name}' - it has {len(course.rounds)} associated round(s)")

        db.session.delete(course)
        db.session.commit()
        return True

    @staticmethod
    def search_courses(query: str) -> List[Dict[str, Any]]:
        """
        Search courses by name or club name.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching course dictionaries
        """
        courses = Course.query.join(Club).filter(
            db.or_(
                Course.name.ilike(f'%{query}%'),
                Club.name.ilike(f'%{query}%')
            )
        ).all()
        
        return [course.to_dict() for course in courses]

    @staticmethod
    def get_course_with_full_details(course_id: int) -> Optional[Dict[str, Any]]:
        """
        Get course with complete hole and tee set information.
        
        Args:
            course_id: The course ID
            
        Returns:
            Complete course dictionary or None if not found
        """
        course = Course.query.get(course_id)
        if not course:
            return None
            
        course_data = course.to_dict(include_holes=True, include_tee_sets=True)
        
        # Add club information
        if course.club:
            course_data['club'] = course.club.to_dict()
            
        return course_data

    @staticmethod
    def set_default_tee_set(course_id: int, tee_set_id: int) -> Optional[Dict[str, Any]]:
        """
        Set the default tee set for a course.
        
        Args:
            course_id: The course ID
            tee_set_id: The tee set ID
            
        Returns:
            Updated course dictionary or None if not found
            
        Raises:
            ValueError: If tee set doesn't belong to course
        """
        course = Course.query.get(course_id)
        if not course:
            return None
            
        # Verify tee set belongs to this course
        from app.models.tee_set import TeeSet
        tee_set = TeeSet.query.filter_by(id=tee_set_id, course_id=course_id).first()
        if not tee_set:
            raise ValueError("Tee set not found or doesn't belong to this course")
            
        course.default_tee_set_id = tee_set_id
        db.session.commit()
        
        return course.to_dict() 