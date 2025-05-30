"""
Score Service

Contains all business logic for score operations.
Simple and focused on core golf scoring.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models.score import Score
from app.models.round import Round
from app.models.hole import Hole


class ScoreService:
    """Service class for score business logic"""

    @staticmethod
    def get_scores_by_round(round_id: int) -> List[Dict[str, Any]]:
        """Get all scores for a round, ordered by hole number"""
        scores = Score.query.filter_by(round_id=round_id)\
                          .join(Hole)\
                          .order_by(Hole.hole_number).all()
        return [score.to_dict() for score in scores]

    @staticmethod
    def get_score_by_id(score_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific score by ID"""
        score = Score.query.get(score_id)
        return score.to_dict() if score else None

    @staticmethod
    def create_score(score_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new score"""
        # Validate required fields
        required_fields = ['round_id', 'hole_id', 'strokes']
        for field in required_fields:
            if field not in score_data:
                raise ValueError(f"{field} is required")
        
        # Validate strokes
        strokes = score_data['strokes']
        if strokes < 1 or strokes > 20:  # Reasonable range
            raise ValueError("Strokes must be between 1 and 20")
        
        # Verify round and hole exist
        round = Round.query.get(score_data['round_id'])
        if not round:
            raise ValueError("Round not found")
            
        hole = Hole.query.get(score_data['hole_id'])
        if not hole:
            raise ValueError("Hole not found")
            
        # Verify hole belongs to round's course
        if hole.course_id != round.course_id:
            raise ValueError("Hole must belong to the round's course")

        try:
            score = Score(
                round_id=score_data['round_id'],
                hole_id=score_data['hole_id'],
                strokes=strokes
            )
            
            # Calculate Stableford points if round has course handicap
            if round.course_handicap:
                score.update_stableford_points(round.course_handicap)
            
            db.session.add(score)
            db.session.commit()
            
            # Update round totals
            round.calculate_totals()
            db.session.commit()
            
            return score.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Score already exists for this hole in this round")

    @staticmethod
    def update_score(score_id: int, score_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing score"""
        score = Score.query.get(score_id)
        if not score:
            return None

        try:
            # Update strokes if provided
            if 'strokes' in score_data:
                strokes = score_data['strokes']
                if strokes < 1 or strokes > 20:
                    raise ValueError("Strokes must be between 1 and 20")
                score.strokes = strokes
                
                # Recalculate Stableford points
                if score.round.course_handicap:
                    score.update_stableford_points(score.round.course_handicap)

            db.session.commit()
            
            # Update round totals
            score.round.calculate_totals()
            db.session.commit()
            
            return score.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Failed to update score due to database constraints")

    @staticmethod
    def delete_score(score_id: int) -> bool:
        """Delete a score"""
        score = Score.query.get(score_id)
        if not score:
            return False

        round = score.round
        db.session.delete(score)
        db.session.commit()
        
        # Update round totals
        round.calculate_totals()
        db.session.commit()
        
        return True

    @staticmethod
    def create_scores_for_holes(round_id: int, hole_scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create multiple scores for a round"""
        # Verify round exists
        round = Round.query.get(round_id)
        if not round:
            raise ValueError("Round not found")
        
        created_scores = []
        
        try:
            for hole_score in hole_scores:
                if 'hole_number' not in hole_score or 'strokes' not in hole_score:
                    raise ValueError("Each score must have 'hole_number' and 'strokes'")
                
                # Find hole by number
                hole = Hole.query.filter_by(
                    course_id=round.course_id, 
                    hole_number=hole_score['hole_number']
                ).first()
                
                if not hole:
                    raise ValueError(f"Hole {hole_score['hole_number']} not found")
                
                # Validate strokes
                strokes = hole_score['strokes']
                if strokes < 1 or strokes > 20:
                    raise ValueError(f"Strokes for hole {hole_score['hole_number']} must be between 1 and 20")
                
                # Create score
                score = Score(
                    round_id=round_id,
                    hole_id=hole.id,
                    strokes=strokes
                )
                
                # Calculate Stableford points
                if round.course_handicap:
                    score.update_stableford_points(round.course_handicap)
                
                db.session.add(score)
                created_scores.append(score)
            
            db.session.commit()
            
            # Update round totals
            round.calculate_totals()
            db.session.commit()
            
            return [score.to_dict() for score in created_scores]
            
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to create scores: {str(e)}")

    @staticmethod
    def recalculate_round_points(round_id: int) -> Dict[str, Any]:
        """Recalculate Stableford points for all scores in a round"""
        round = Round.query.get(round_id)
        if not round:
            raise ValueError("Round not found")
        
        if not round.course_handicap:
            raise ValueError("Round must have a course handicap to calculate points")
        
        # Update all score points
        for score in round.scores:
            score.update_stableford_points(round.course_handicap)
        
        # Update round totals
        round.calculate_totals()
        
        db.session.commit()
        return round.to_dict(include_scores=True) 