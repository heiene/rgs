from datetime import datetime, date
from app.extensions import db

class Handicap(db.Model):
    """
    Handicap Model
    
    Represents a user's handicap history with temporal data management.
    Allows for historical handicap changes and proper date ordering.
    """
    __tablename__ = 'handicaps'

    id = db.Column(db.Integer, primary_key=True)
    handicap_value = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=date.today)
    end_date = db.Column(db.Date, nullable=True)  # NULL means current handicap
    reason = db.Column(db.String(200))  # e.g., "initial", "update from external source", "manual adjustment"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='handicaps', foreign_keys=[user_id])
    created_by = db.relationship('User', back_populates='created_handicaps', foreign_keys=[created_by_id])

    def __repr__(self):
        status = "Current" if self.end_date is None else "Historical"
        return f'<Handicap {self.handicap_value} ({status})>'

    @property
    def is_current(self):
        """Check if this is the current handicap"""
        return self.end_date is None

    @property
    def is_valid_on_date(self, check_date=None):
        """Check if handicap was valid on a specific date"""
        if check_date is None:
            check_date = date.today()
        
        if check_date < self.start_date:
            return False
        
        if self.end_date and check_date > self.end_date:
            return False
            
        return True

    def days_active(self):
        """Get number of days this handicap was/is active"""
        end = self.end_date or date.today()
        return (end - self.start_date).days

    @staticmethod
    def get_handicap_on_date(user_id, check_date=None):
        """Get user's handicap that was valid on a specific date"""
        if check_date is None:
            check_date = date.today()
            
        handicap = Handicap.query.filter(
            Handicap.user_id == user_id,
            Handicap.start_date <= check_date,
            db.or_(
                Handicap.end_date.is_(None),
                Handicap.end_date >= check_date
            )
        ).first()
        
        return handicap

    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'handicap_value': self.handicap_value,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'reason': self.reason,
            'is_current': self.is_current,
            'days_active': self.days_active(),
            'user_id': self.user_id,
            'created_by_id': self.created_by_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }