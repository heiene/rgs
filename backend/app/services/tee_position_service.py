"""
TeePosition Service

Contains all business logic for tee position operations.
Follows the "Fat Services, Thin Routes" pattern.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models.tee_position import TeePosition
from app.models.hole import Hole
from app.models.tee_set import TeeSet


class TeePositionService:
    """Service class for tee position business logic"""

    @staticmethod
    def get_tee_positions_by_tee_set(tee_set_id: int, unit: str = 'meters') -> List[Dict[str, Any]]:
        """
        Get all tee positions for a specific tee set.
        
        Args:
            tee_set_id: The tee set ID
            unit: Distance unit ('meters' or 'yards')
            
        Returns:
            List of tee position dictionaries ordered by hole number
        """
        positions = TeePosition.query.filter_by(tee_set_id=tee_set_id).join(Hole).order_by(Hole.hole_number).all()
        return [position.to_dict(unit=unit) for position in positions]

    @staticmethod
    def get_tee_positions_by_hole(hole_id: int, unit: str = 'meters') -> List[Dict[str, Any]]:
        """
        Get all tee positions for a specific hole.
        
        Args:
            hole_id: The hole ID
            unit: Distance unit ('meters' or 'yards')
            
        Returns:
            List of tee position dictionaries
        """
        positions = TeePosition.query.filter_by(hole_id=hole_id).all()
        return [position.to_dict(unit=unit) for position in positions]

    @staticmethod
    def get_tee_position_by_id(position_id: int, unit: str = 'meters') -> Optional[Dict[str, Any]]:
        """
        Get a specific tee position by ID.
        
        Args:
            position_id: The tee position ID
            unit: Distance unit ('meters' or 'yards')
            
        Returns:
            Tee position dictionary or None if not found
        """
        position = TeePosition.query.get(position_id)
        return position.to_dict(unit=unit) if position else None

    @staticmethod
    def create_tee_position(position_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new tee position.
        
        Args:
            position_data: Dictionary containing tee position information
            
        Returns:
            Created tee position dictionary
            
        Raises:
            ValueError: If position data is invalid
        """
        # Validate required fields
        required_fields = ['hole_id', 'tee_set_id', 'length']
        for field in required_fields:
            if field not in position_data:
                raise ValueError(f"{field} is required")
        
        # Verify hole exists
        hole = Hole.query.get(position_data['hole_id'])
        if not hole:
            raise ValueError("Hole not found")
        
        # Verify tee set exists
        tee_set = TeeSet.query.get(position_data['tee_set_id'])
        if not tee_set:
            raise ValueError("Tee set not found")
        
        # Verify tee set belongs to same course as hole
        if hole.course_id != tee_set.course_id:
            raise ValueError("Hole and tee set must belong to the same course")
        
        # Validate length (reasonable golf hole distances)
        length = position_data['length']
        if length < 50 or length > 700:  # 50m to 700m (extreme range)
            raise ValueError("Length must be between 50 and 700 meters")

        try:
            position = TeePosition(
                hole_id=position_data['hole_id'],
                tee_set_id=position_data['tee_set_id'],
                length=length
            )
            
            db.session.add(position)
            db.session.commit()
            
            return position.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Tee position already exists for this hole and tee set combination")

    @staticmethod
    def update_tee_position(position_id: int, position_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing tee position.
        
        Args:
            position_id: The tee position ID
            position_data: Dictionary containing updated position information
            
        Returns:
            Updated tee position dictionary or None if not found
            
        Raises:
            ValueError: If position data is invalid
        """
        position = TeePosition.query.get(position_id)
        if not position:
            return None

        try:
            # Update length if provided
            if 'length' in position_data:
                length = position_data['length']
                if length < 50 or length > 700:
                    raise ValueError("Length must be between 50 and 700 meters")
                position.length = length

            db.session.commit()
            return position.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Failed to update tee position due to database constraints")

    @staticmethod
    def delete_tee_position(position_id: int) -> bool:
        """
        Delete a tee position.
        
        Args:
            position_id: The tee position ID
            
        Returns:
            True if deleted, False if not found
        """
        position = TeePosition.query.get(position_id)
        if not position:
            return False

        db.session.delete(position)
        db.session.commit()
        return True

    @staticmethod
    def create_tee_positions_for_tee_set(tee_set_id: int, distances: List[int]) -> List[Dict[str, Any]]:
        """
        Create tee positions for all holes in a tee set.
        
        Args:
            tee_set_id: The tee set ID
            distances: List of distances in meters (one per hole)
            
        Returns:
            List of created tee position dictionaries
            
        Raises:
            ValueError: If tee set not found or invalid data
        """
        # Verify tee set exists
        tee_set = TeeSet.query.get(tee_set_id)
        if not tee_set:
            raise ValueError("Tee set not found")
        
        # Get course holes
        holes = Hole.query.filter_by(course_id=tee_set.course_id).order_by(Hole.hole_number).all()
        
        if len(distances) != len(holes):
            raise ValueError(f"Number of distances ({len(distances)}) must match number of holes ({len(holes)})")
        
        # Check if tee set already has positions
        existing_positions = TeePosition.query.filter_by(tee_set_id=tee_set_id).count()
        if existing_positions > 0:
            raise ValueError("Tee set already has positions")

        created_positions = []
        
        try:
            for i, hole in enumerate(holes):
                position_data = {
                    'hole_id': hole.id,
                    'tee_set_id': tee_set_id,
                    'length': distances[i]
                }
                
                position = TeePosition(
                    hole_id=hole.id,
                    tee_set_id=tee_set_id,
                    length=distances[i]
                )
                
                db.session.add(position)
                created_positions.append(position)
            
            db.session.commit()
            return [position.to_dict() for position in created_positions]
            
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to create tee positions: {str(e)}")

    @staticmethod
    def create_standard_distances_by_par(tee_set_id: int, difficulty_level: str = 'medium') -> List[Dict[str, Any]]:
        """
        Create standard distances based on hole par and difficulty level.
        
        Args:
            tee_set_id: The tee set ID
            difficulty_level: 'easy', 'medium', 'hard', or 'championship'
            
        Returns:
            List of created tee position dictionaries
            
        Raises:
            ValueError: If invalid data
        """
        # Distance ranges by par and difficulty (in meters)
        distance_ranges = {
            'easy': {3: (110, 140), 4: (280, 320), 5: (400, 450), 6: (500, 550)},
            'medium': {3: (130, 160), 4: (320, 360), 5: (450, 500), 6: (550, 600)},
            'hard': {3: (150, 180), 4: (360, 400), 5: (500, 550), 6: (600, 650)},
            'championship': {3: (170, 200), 4: (400, 440), 5: (550, 600), 6: (650, 700)}
        }
        
        if difficulty_level not in distance_ranges:
            raise ValueError("Difficulty level must be 'easy', 'medium', 'hard', or 'championship'")
        
        # Verify tee set exists
        tee_set = TeeSet.query.get(tee_set_id)
        if not tee_set:
            raise ValueError("Tee set not found")
        
        # Get course holes
        holes = Hole.query.filter_by(course_id=tee_set.course_id).order_by(Hole.hole_number).all()
        
        if not holes:
            raise ValueError("Course has no holes")
        
        # Generate distances based on par
        distances = []
        ranges = distance_ranges[difficulty_level]
        
        for hole in holes:
            if hole.par in ranges:
                min_dist, max_dist = ranges[hole.par]
                # Use stroke index to vary within range (harder holes = longer)
                factor = (hole.stroke_index - 1) / 17  # 0 to 1
                distance = int(min_dist + factor * (max_dist - min_dist))
                distances.append(distance)
            else:
                # Fallback for unusual par values
                distances.append(300)
        
        return TeePositionService.create_tee_positions_for_tee_set(tee_set_id, distances)

    @staticmethod
    def get_tee_position_statistics(tee_set_id: int) -> Optional[Dict[str, Any]]:
        """
        Get statistics for tee positions of a tee set.
        
        Args:
            tee_set_id: The tee set ID
            
        Returns:
            Dictionary with tee position statistics
        """
        tee_set = TeeSet.query.get(tee_set_id)
        if not tee_set:
            return None
        
        positions = TeePosition.query.filter_by(tee_set_id=tee_set_id).join(Hole).all()
        
        if not positions:
            return {
                'tee_set_id': tee_set_id,
                'total_positions': 0,
                'total_length_meters': 0,
                'total_length_yards': 0,
                'average_distance': 0,
                'shortest_hole': None,
                'longest_hole': None
            }
        
        distances = [pos.length for pos in positions]
        total_meters = sum(distances)
        
        shortest_pos = min(positions, key=lambda x: x.length)
        longest_pos = max(positions, key=lambda x: x.length)
        
        return {
            'tee_set_id': tee_set_id,
            'tee_set_name': tee_set.name,
            'total_positions': len(positions),
            'total_length_meters': total_meters,
            'total_length_yards': round(total_meters * 1.09361),
            'average_distance': round(total_meters / len(positions)),
            'shortest_hole': {
                'hole_number': shortest_pos.hole.hole_number,
                'par': shortest_pos.hole.par,
                'distance_meters': shortest_pos.length,
                'distance_yards': shortest_pos.length_in_yards()
            },
            'longest_hole': {
                'hole_number': longest_pos.hole.hole_number,
                'par': longest_pos.hole.par,
                'distance_meters': longest_pos.length,
                'distance_yards': longest_pos.length_in_yards()
            },
            'distance_breakdown': {
                'par_3': [pos.length for pos in positions if pos.hole.par == 3],
                'par_4': [pos.length for pos in positions if pos.hole.par == 4],
                'par_5': [pos.length for pos in positions if pos.hole.par == 5]
            }
        }

    @staticmethod
    def bulk_update_distances(tee_set_id: int, distances: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Bulk update distances for a tee set.
        
        Args:
            tee_set_id: The tee set ID
            distances: List of dicts with 'hole_number' and 'length'
            
        Returns:
            List of updated tee position dictionaries
            
        Raises:
            ValueError: If invalid data
        """
        # Verify tee set exists
        tee_set = TeeSet.query.get(tee_set_id)
        if not tee_set:
            raise ValueError("Tee set not found")
        
        updated_positions = []
        
        try:
            for distance_update in distances:
                hole_number = distance_update.get('hole_number')
                new_length = distance_update.get('length')
                
                if hole_number is None or new_length is None:
                    raise ValueError("Each distance update must have 'hole_number' and 'length'")
                
                # Find the hole
                hole = Hole.query.filter_by(course_id=tee_set.course_id, hole_number=hole_number).first()
                if not hole:
                    raise ValueError(f"Hole {hole_number} not found")
                
                # Find the tee position
                position = TeePosition.query.filter_by(tee_set_id=tee_set_id, hole_id=hole.id).first()
                if not position:
                    raise ValueError(f"Tee position for hole {hole_number} not found")
                
                # Validate length
                if new_length < 50 or new_length > 700:
                    raise ValueError(f"Length for hole {hole_number} must be between 50 and 700 meters")
                
                # Update length
                position.length = new_length
                updated_positions.append(position)
            
            db.session.commit()
            return [position.to_dict() for position in updated_positions]
            
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to bulk update distances: {str(e)}") 