"""
Hole Service

Contains all business logic for hole operations.
Follows the "Fat Services, Thin Routes" pattern.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models.hole import Hole
from app.models.course import Course


class HoleService:
    """Service class for hole business logic"""

    @staticmethod
    def get_holes_by_course(course_id: int, include_tee_positions: bool = False) -> List[Dict[str, Any]]:
        """
        Get all holes for a specific course.
        
        Args:
            course_id: The course ID
            include_tee_positions: Whether to include tee position data
            
        Returns:
            List of hole dictionaries ordered by hole number
        """
        holes = Hole.query.filter_by(course_id=course_id).order_by(Hole.hole_number).all()
        return [hole.to_dict(include_tee_positions=include_tee_positions) for hole in holes]

    @staticmethod
    def get_hole_by_id(hole_id: int, include_tee_positions: bool = False) -> Optional[Dict[str, Any]]:
        """
        Get a specific hole by ID.
        
        Args:
            hole_id: The hole ID
            include_tee_positions: Whether to include tee position data
            
        Returns:
            Hole dictionary or None if not found
        """
        hole = Hole.query.get(hole_id)
        return hole.to_dict(include_tee_positions=include_tee_positions) if hole else None

    @staticmethod
    def create_hole(hole_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new hole.
        
        Args:
            hole_data: Dictionary containing hole information
            
        Returns:
            Created hole dictionary
            
        Raises:
            ValueError: If hole data is invalid
        """
        # Validate required fields
        required_fields = ['hole_number', 'par', 'stroke_index', 'course_id']
        for field in required_fields:
            if field not in hole_data:
                raise ValueError(f"{field} is required")
        
        # Verify course exists
        course = Course.query.get(hole_data['course_id'])
        if not course:
            raise ValueError("Course not found")
        
        # Validate hole number is within course limits
        hole_number = hole_data['hole_number']
        if hole_number < 1 or hole_number > course.holes_count:
            raise ValueError(f"Hole number must be between 1 and {course.holes_count}")
        
        # Validate par (typically 3, 4, or 5)
        par = hole_data['par']
        if par < 3 or par > 6:
            raise ValueError("Par must be between 3 and 6")
        
        # Validate stroke index (1-18 for difficulty ranking)
        stroke_index = hole_data['stroke_index']
        if stroke_index < 1 or stroke_index > 18:
            raise ValueError("Stroke index must be between 1 and 18")

        try:
            hole = Hole(
                hole_number=hole_number,
                par=par,
                stroke_index=stroke_index,
                course_id=hole_data['course_id']
            )
            
            db.session.add(hole)
            db.session.commit()
            
            return hole.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError(f"Hole {hole_number} already exists for this course")

    @staticmethod
    def update_hole(hole_id: int, hole_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing hole.
        
        Args:
            hole_id: The hole ID
            hole_data: Dictionary containing updated hole information
            
        Returns:
            Updated hole dictionary or None if not found
            
        Raises:
            ValueError: If hole data is invalid
        """
        hole = Hole.query.get(hole_id)
        if not hole:
            return None

        try:
            # Update fields if provided
            if 'hole_number' in hole_data:
                hole_number = hole_data['hole_number']
                if hole_number < 1 or hole_number > hole.course.holes_count:
                    raise ValueError(f"Hole number must be between 1 and {hole.course.holes_count}")
                hole.hole_number = hole_number
            
            if 'par' in hole_data:
                par = hole_data['par']
                if par < 3 or par > 6:
                    raise ValueError("Par must be between 3 and 6")
                hole.par = par
            
            if 'stroke_index' in hole_data:
                stroke_index = hole_data['stroke_index']
                if stroke_index < 1 or stroke_index > 18:
                    raise ValueError("Stroke index must be between 1 and 18")
                hole.stroke_index = stroke_index

            db.session.commit()
            return hole.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Hole number already exists for this course")

    @staticmethod
    def delete_hole(hole_id: int) -> bool:
        """
        Delete a hole.
        
        Args:
            hole_id: The hole ID
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            ValueError: If hole has associated scores
        """
        hole = Hole.query.get(hole_id)
        if not hole:
            return False

        # Check if hole has scores
        if hole.scores:
            raise ValueError(f"Cannot delete hole {hole.hole_number} - it has {len(hole.scores)} associated score(s)")

        db.session.delete(hole)
        db.session.commit()
        return True

    @staticmethod
    def create_standard_18_holes(course_id: int, par_layout: List[int] = None) -> List[Dict[str, Any]]:
        """
        Create standard 18 holes for a course.
        
        Args:
            course_id: The course ID
            par_layout: List of 18 par values (defaults to balanced layout)
            
        Returns:
            List of created hole dictionaries
            
        Raises:
            ValueError: If course already has holes or invalid data
        """
        # Verify course exists
        course = Course.query.get(course_id)
        if not course:
            raise ValueError("Course not found")
        
        # Check if course already has holes
        existing_holes = Hole.query.filter_by(course_id=course_id).count()
        if existing_holes > 0:
            raise ValueError("Course already has holes")
        
        # Default balanced par layout if not provided
        if par_layout is None:
            # Standard layout: 4 par 3s, 10 par 4s, 4 par 5s = 72 total par
            par_layout = [4, 4, 3, 4, 5, 4, 3, 4, 4,  # Front 9
                         4, 5, 4, 3, 4, 5, 4, 3, 5]   # Back 9
        
        if len(par_layout) != 18:
            raise ValueError("Par layout must contain exactly 18 values")
        
        # Standard stroke index (difficulty) distribution
        stroke_indices = [1, 3, 17, 5, 15, 7, 11, 9, 13,    # Front 9
                         2, 16, 4, 18, 6, 14, 8, 12, 10]    # Back 9
        
        created_holes = []
        
        try:
            for i in range(18):
                hole_data = {
                    'hole_number': i + 1,
                    'par': par_layout[i],
                    'stroke_index': stroke_indices[i],
                    'course_id': course_id
                }
                
                hole = Hole(
                    hole_number=hole_data['hole_number'],
                    par=hole_data['par'],
                    stroke_index=hole_data['stroke_index'],
                    course_id=hole_data['course_id']
                )
                
                db.session.add(hole)
                created_holes.append(hole)
            
            db.session.commit()
            return [hole.to_dict() for hole in created_holes]
            
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to create holes: {str(e)}")

    @staticmethod
    def get_hole_statistics(hole_id: int) -> Dict[str, Any]:
        """
        Get statistics for a specific hole.
        
        Args:
            hole_id: The hole ID
            
        Returns:
            Dictionary with hole statistics
        """
        hole = Hole.query.get(hole_id)
        if not hole:
            return None
        
        # Basic hole info
        stats = hole.to_dict(include_tee_positions=True)
        
        # Add scoring statistics if there are scores
        if hole.scores:
            scores = [score.strokes for score in hole.scores]
            stats['scoring_stats'] = {
                'total_rounds': len(scores),
                'average_score': round(sum(scores) / len(scores), 2),
                'best_score': min(scores),
                'worst_score': max(scores),
                'eagles_or_better': len([s for s in scores if s <= hole.par - 2]),
                'birdies': len([s for s in scores if s == hole.par - 1]),
                'pars': len([s for s in scores if s == hole.par]),
                'bogeys': len([s for s in scores if s == hole.par + 1]),
                'double_bogeys_or_worse': len([s for s in scores if s >= hole.par + 2])
            }
        else:
            stats['scoring_stats'] = None
            
        return stats

    @staticmethod
    def validate_course_holes(course_id: int) -> Dict[str, Any]:
        """
        Validate that a course has proper hole setup.
        
        Args:
            course_id: The course ID
            
        Returns:
            Dictionary with validation results
        """
        course = Course.query.get(course_id)
        if not course:
            return {"valid": False, "error": "Course not found"}
        
        holes = Hole.query.filter_by(course_id=course_id).all()
        
        validation = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "hole_count": len(holes),
            "expected_holes": course.holes_count
        }
        
        # Check hole count
        if len(holes) != course.holes_count:
            validation["valid"] = False
            validation["errors"].append(f"Expected {course.holes_count} holes, found {len(holes)}")
        
        if holes:
            # Check hole numbers are sequential
            hole_numbers = sorted([hole.hole_number for hole in holes])
            expected_numbers = list(range(1, course.holes_count + 1))
            
            if hole_numbers != expected_numbers:
                validation["valid"] = False
                validation["errors"].append(f"Hole numbers are not sequential: {hole_numbers}")
            
            # Check stroke indices are unique and in proper range
            stroke_indices = [hole.stroke_index for hole in holes]
            if len(set(stroke_indices)) != len(stroke_indices):
                validation["warnings"].append("Stroke indices are not unique")
            
            # Calculate total par
            total_par = sum(hole.par for hole in holes)
            validation["total_par"] = total_par
            
            # Check if par is reasonable for course type
            if course.holes_count == 18:
                if total_par < 68 or total_par > 76:
                    validation["warnings"].append(f"Total par {total_par} is unusual for 18-hole course")
        
        return validation 