from datetime import datetime
from app.extensions import db

class Club(db.Model):
    """
    Club Model
    
    Represents a golf club which can have multiple courses.
    Example: Augusta National Golf Club (club) has multiple courses.
    """
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text)
    website = db.Column(db.String(200))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    timezone = db.Column(db.String(50), nullable=False, default='Europe/Oslo')  # IANA timezone identifier
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    courses = db.relationship('Course', back_populates='club', cascade='all, delete-orphan')
    members = db.relationship('User', back_populates='home_club')

    def __repr__(self):
        return f'<Club {self.name}>'

    @property
    def full_address(self):
        """Get club's full address"""
        parts = [self.address, self.city, self.postal_code, self.country]
        return ', '.join(part for part in parts if part)

    def get_localized_timezone(self):
        """Get club's timezone for localized timestamps"""
        return self.timezone

    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'website': self.website,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'postal_code': self.postal_code,
            'timezone': self.timezone,
            'full_address': self.full_address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
