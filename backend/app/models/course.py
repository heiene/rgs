from datetime import datetime
from app.extensions import db

class Course(db.Model):
    """
    Course Model
    
    Represents a golf course within a club.
    A club can have multiple courses, each with their own holes and tee sets.
    """
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    holes_count = db.Column(db.Integer, nullable=False, default=18)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    default_tee_set_id = db.Column(db.Integer, db.ForeignKey('tee_sets.id'), nullable=True)

    # Relationships
    club = db.relationship('Club', back_populates='courses')
    holes = db.relationship('Hole', back_populates='course', cascade='all, delete-orphan')
    tee_sets = db.relationship('TeeSet', back_populates='course', cascade='all, delete-orphan', 
                              foreign_keys='TeeSet.course_id')
    default_tee_set = db.relationship('TeeSet', foreign_keys=[default_tee_set_id], post_update=True)
    rounds = db.relationship('Round', back_populates='course')

    def __repr__(self):
        return f'<Course {self.name}>'

    @property
    def total_par(self):
        """Get total par for the course"""
        return sum(hole.par for hole in self.holes)

    def to_dict(self, include_holes=False, include_tee_sets=False):
        """Convert model to dictionary for JSON serialization"""
        data = {
            'id': self.id,
            'name': self.name,
            'holes_count': self.holes_count,
            'description': self.description,
            'club_id': self.club_id,
            'default_tee_set_id': self.default_tee_set_id,
            'total_par': self.total_par,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_holes:
            data['holes'] = [hole.to_dict() for hole in self.holes]
            
        if include_tee_sets:
            data['tee_sets'] = [tee_set.to_dict() for tee_set in self.tee_sets]
            
        return data