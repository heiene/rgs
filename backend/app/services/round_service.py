"""
Round Service

Contains all business logic for round operations.
Simple and focused on core golf functionality.
"""
from typing import List, Optional, Dict, Any
from datetime import date
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models.round import Round
from app.models.user import User
from app.models.course import Course
from app.models.tee_set import TeeSet


class RoundService:
    """Service class for round business logic"""

    @staticmethod
    def get_rounds_by_user(user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent rounds for a user"""
        rounds = Round.query.filter_by(user_id=user_id)\
                          .order_by(Round.date_played.desc())\
                          .limit(limit).all()
        return [round.to_dict() for round in rounds]

    @staticmethod
    def get_round_by_id(round_id: int, include_scores: bool = False) -> Optional[Dict[str, Any]]:
        """Get a specific round by ID"""
        round = Round.query.get(round_id)
        return round.to_dict(include_scores=include_scores) if round else None

    @staticmethod
    def create_round(round_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new round"""
        # Validate required fields
        required_fields = ['user_id', 'course_id', 'tee_set_id']
        for field in required_fields:
            if field not in round_data:
                raise ValueError(f"{field} is required")
        
        # Verify relationships exist
        user = User.query.get(round_data['user_id'])
        if not user:
            raise ValueError("User not found")
            
        course = Course.query.get(round_data['course_id'])
        if not course:
            raise ValueError("Course not found")
            
        tee_set = TeeSet.query.get(round_data['tee_set_id'])
        if not tee_set:
            raise ValueError("Tee set not found")
            
        # Verify tee set belongs to course
        if tee_set.course_id != course.id:
            raise ValueError("Tee set must belong to the selected course")

        try:
            round = Round(
                user_id=round_data['user_id'],
                course_id=round_data['course_id'],
                tee_set_id=round_data['tee_set_id'],
                date_played=round_data.get('date_played', date.today()),
                handicap_used=round_data.get('handicap_used')
            )
            
            # Stamp course/slope ratings from tee set
            round.stamp_ratings_from_tee_set()
            
            # Calculate course handicap if handicap_used provided
            if round.handicap_used:
                round.course_handicap = round.calculate_course_handicap()
            
            db.session.add(round)
            db.session.commit()
            
            return round.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Failed to create round due to database constraints")

    @staticmethod
    def update_round(round_id: int, round_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing round"""
        round = Round.query.get(round_id)
        if not round:
            return None

        try:
            # Update allowed fields
            if 'date_played' in round_data:
                round.date_played = round_data['date_played']
            
            if 'handicap_used' in round_data:
                round.handicap_used = round_data['handicap_used']
                if round.handicap_used:
                    round.course_handicap = round.calculate_course_handicap()

            # Recalculate totals from scores
            round.calculate_totals()
            
            db.session.commit()
            return round.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Failed to update round due to database constraints")

    @staticmethod
    def delete_round(round_id: int) -> bool:
        """Delete a round and all its scores"""
        round = Round.query.get(round_id)
        if not round:
            return False

        db.session.delete(round)
        db.session.commit()
        return True

    @staticmethod
    def finalize_round(round_id: int) -> Optional[Dict[str, Any]]:
        """Finalize a round by calculating all totals and differential"""
        round = Round.query.get(round_id)
        if not round:
            return None
        
        # Calculate totals from scores
        round.calculate_totals()
        
        # Update Stableford points for all scores if course handicap exists
        if round.course_handicap:
            for score in round.scores:
                score.update_stableford_points(round.course_handicap)
        
        db.session.commit()
        return round.to_dict(include_scores=True)

    @staticmethod
    def get_user_stats(user_id: int) -> Dict[str, Any]:
        """Get basic statistics for a user's rounds"""
        rounds = Round.query.filter_by(user_id=user_id).all()
        completed_rounds = [r for r in rounds if r.is_complete]
        
        if not completed_rounds:
            return {
                'total_rounds': len(rounds),
                'completed_rounds': 0,
                'average_score': None,
                'best_score': None,
                'latest_differential': None
            }
        
        scores = [r.total_score for r in completed_rounds if r.total_score]
        differentials = [r.differential for r in completed_rounds if r.differential]
        
        return {
            'total_rounds': len(rounds),
            'completed_rounds': len(completed_rounds),
            'average_score': round(sum(scores) / len(scores), 1) if scores else None,
            'best_score': min(scores) if scores else None,
            'latest_differential': differentials[-1] if differentials else None
        } 