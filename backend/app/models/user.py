from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(db.Model):
    """
    User Model
    
    Represents a golf player with authentication, preferences, and club membership.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(1), nullable=False, default='M')  # 'M' or 'F'
    
    # Account status
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Password reset
    password_reset_token = db.Column(db.String(255))
    password_reset_expires = db.Column(db.DateTime)
    
    # Preferences
    distance_unit = db.Column(db.String(10), nullable=False, default='meters')  # 'meters' or 'yards'
    
    # Location and timezone
    timezone = db.Column(db.String(50), nullable=False, default='Europe/Oslo')  # IANA timezone identifier
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    address = db.Column(db.String(200))
    postal_code = db.Column(db.String(20))
    
    # Foreign Keys
    home_club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=True)
    preferred_theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'), nullable=True)

    # Relationships
    home_club = db.relationship('Club', back_populates='members')
    preferred_theme = db.relationship('Theme', back_populates='users')
    rounds = db.relationship('Round', back_populates='user', cascade='all, delete-orphan')
    handicaps = db.relationship('Handicap', foreign_keys='Handicap.user_id', back_populates='user', cascade='all, delete-orphan')
    created_handicaps = db.relationship('Handicap', foreign_keys='Handicap.created_by_id', back_populates='created_by')

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"

    @property
    def current_handicap(self):
        """Get user's current handicap"""
        from app.models.handicap import Handicap
        current = Handicap.query.filter(
            Handicap.user_id == self.id,
            Handicap.end_date.is_(None)
        ).first()
        return current.handicap_value if current else None

    @property
    def full_address(self):
        """Get user's full address"""
        parts = [self.address, self.city, self.postal_code, self.country]
        return ', '.join(part for part in parts if part)

    def get_localized_timezone(self):
        """Get user's timezone for localized timestamps"""
        return self.timezone

    def to_dict(self, include_sensitive=False):
        """Convert model to dictionary for JSON serialization"""
        data = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'sex': self.sex,
            'is_active': self.is_active,
            'distance_unit': self.distance_unit,
            'timezone': self.timezone,
            'country': self.country,
            'city': self.city,
            'address': self.address,
            'postal_code': self.postal_code,
            'full_address': self.full_address,
            'home_club_id': self.home_club_id,
            'preferred_theme_id': self.preferred_theme_id,
            'current_handicap': self.current_handicap,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        
        if include_sensitive:
            data.update({
                'is_admin': self.is_admin,
                'password_reset_token': self.password_reset_token,
                'password_reset_expires': self.password_reset_expires.isoformat() if self.password_reset_expires else None
            })
            
        return data
