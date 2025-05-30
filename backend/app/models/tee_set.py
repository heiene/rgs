from datetime import datetime
from app.extensions import db

class TeeSet(db.Model):
    """
    TeeSet Model
    
    Represents a set of tees for a course (e.g., "Yellow", "Red", "Championship").
    Contains course and slope ratings for handicap calculations.
    """
    __tablename__ = 'tee_sets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # e.g., "Yellow", "58", "Red"
    
    # Men's ratings (mandatory)
    slope_rating = db.Column(db.Float, nullable=False)
    course_rating = db.Column(db.Float, nullable=False)
    
    # Women's ratings (optional)
    women_slope_rating = db.Column(db.Float, nullable=True)
    women_course_rating = db.Column(db.Float, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    # Relationships
    course = db.relationship('Course', back_populates='tee_sets', foreign_keys=[course_id])
    tee_positions = db.relationship('TeePosition', back_populates='tee_set', cascade='all, delete-orphan')
    rounds = db.relationship('Round', back_populates='tee_set')

    def __repr__(self):
        return f'<TeeSet {self.name} - {self.course.name if self.course else "No Course"}>'

    def get_rating_for_gender(self, gender='M'):
        """Get course and slope rating for specific gender"""
        if gender == 'F' and self.women_course_rating and self.women_slope_rating:
            return {
                'course_rating': self.women_course_rating,
                'slope_rating': self.women_slope_rating
            }
        return {
            'course_rating': self.course_rating,
            'slope_rating': self.slope_rating
        }

    @property
    def total_length_meters(self):
        """Get total length of all holes in meters"""
        return sum(pos.length for pos in self.tee_positions if pos.length)

    def to_dict(self, include_positions=False):
        """Convert model to dictionary for JSON serialization"""
        data = {
            'id': self.id,
            'name': self.name,
            'slope_rating': self.slope_rating,
            'course_rating': self.course_rating,
            'women_slope_rating': self.women_slope_rating,
            'women_course_rating': self.women_course_rating,
            'course_id': self.course_id,
            'total_length_meters': self.total_length_meters,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_positions:
            data['tee_positions'] = [pos.to_dict() for pos in self.tee_positions]
            
        return data