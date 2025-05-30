from datetime import datetime
from app.extensions import db

class Hole(db.Model):
    """
    Hole Model
    
    Represents a single hole on a golf course.
    Contains par and stroke index information.
    """
    __tablename__ = 'holes'

    id = db.Column(db.Integer, primary_key=True)
    hole_number = db.Column(db.Integer, nullable=False)
    par = db.Column(db.Integer, nullable=False)
    stroke_index = db.Column(db.Integer, nullable=False)  # Hole stroke index (1-18, difficulty ranking)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    # Relationships
    course = db.relationship('Course', back_populates='holes')
    tee_positions = db.relationship('TeePosition', back_populates='hole', cascade='all, delete-orphan')
    scores = db.relationship('Score', back_populates='hole')

    # Unique constraint to prevent duplicate hole numbers per course
    __table_args__ = (
        db.UniqueConstraint('course_id', 'hole_number', name='unique_hole_per_course'),
    )

    def __repr__(self):
        return f'<Hole {self.hole_number} - Par {self.par}>'

    def get_length_for_tee_set(self, tee_set_id):
        """Get the length of this hole for a specific tee set"""
        position = next((pos for pos in self.tee_positions if pos.tee_set_id == tee_set_id), None)
        return position.length if position else None

    def to_dict(self, include_tee_positions=False):
        """Convert model to dictionary for JSON serialization"""
        data = {
            'id': self.id,
            'hole_number': self.hole_number,
            'par': self.par,
            'stroke_index': self.stroke_index,
            'course_id': self.course_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_tee_positions:
            data['tee_positions'] = [pos.to_dict() for pos in self.tee_positions]
            
        return data