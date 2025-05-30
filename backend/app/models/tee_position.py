from datetime import datetime
from app.extensions import db

class TeePosition(db.Model):
    """
    TeePosition Model
    
    Represents the distance from a specific tee set to a specific hole.
    This is the junction table between TeeSet and Hole with distance data.
    """
    __tablename__ = 'tee_positions'

    id = db.Column(db.Integer, primary_key=True)
    length = db.Column(db.Integer, nullable=False)  # Length in meters
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    hole_id = db.Column(db.Integer, db.ForeignKey('holes.id'), nullable=False)
    tee_set_id = db.Column(db.Integer, db.ForeignKey('tee_sets.id'), nullable=False)

    # Relationships
    hole = db.relationship('Hole', back_populates='tee_positions')
    tee_set = db.relationship('TeeSet', back_populates='tee_positions')

    # Unique constraint to prevent duplicate tee positions
    __table_args__ = (
        db.UniqueConstraint('hole_id', 'tee_set_id', name='unique_tee_position'),
    )

    def __repr__(self):
        return f'<TeePosition Hole {self.hole.hole_number if self.hole else "?"} - {self.length}m>'

    def length_in_yards(self):
        """Convert length to yards"""
        return round(self.length * 1.09361, 1) if self.length else None

    def get_length_in_unit(self, unit='meters'):
        """Get length in specified unit"""
        if unit == 'yards':
            return self.length_in_yards()
        return self.length

    def to_dict(self, unit='meters'):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'length': self.get_length_in_unit(unit),
            'length_unit': unit,
            'length_meters': self.length,
            'length_yards': self.length_in_yards(),
            'hole_id': self.hole_id,
            'tee_set_id': self.tee_set_id,
            'hole_number': self.hole.hole_number if self.hole else None,
            'par': self.hole.par if self.hole else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }