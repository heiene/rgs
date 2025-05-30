from datetime import datetime, date
from app.extensions import db

class Round(db.Model):
    """
    Round Model
    
    Represents a complete round of golf played by a user.
    Contains scoring, handicap calculations, and Stableford points.
    """
    __tablename__ = 'rounds'

    id = db.Column(db.Integer, primary_key=True)
    date_played = db.Column(db.Date, nullable=False, default=date.today)
    
    # Handicap information (stamped at time of round)
    handicap_used = db.Column(db.Float, nullable=True)  # The handicap used for this round
    course_handicap = db.Column(db.Integer, nullable=True)  # Playing handicap for this course/tee
    
    # Course ratings (stamped to preserve historical accuracy)
    course_rating = db.Column(db.Float, nullable=True)
    slope_rating = db.Column(db.Float, nullable=True)
    
    # Scoring totals
    total_score = db.Column(db.Integer, nullable=True)  # Total strokes
    total_points = db.Column(db.Integer, nullable=True)  # Total Stableford points
    differential = db.Column(db.Float, nullable=True)  # Handicap differential = (Score - Course Rating) * 113 / Slope Rating
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    tee_set_id = db.Column(db.Integer, db.ForeignKey('tee_sets.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='rounds')
    course = db.relationship('Course', back_populates='rounds')
    tee_set = db.relationship('TeeSet', back_populates='rounds')
    scores = db.relationship('Score', back_populates='round', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Round {self.user.email if self.user else "?"} - {self.date_played}>'

    @property
    def is_complete(self):
        """Check if the round is complete (has scores for all holes)"""
        expected_holes = self.course.holes_count if self.course else 18
        return len(self.scores) == expected_holes

    @property
    def net_score(self):
        """Calculate net score (gross score - course handicap)"""
        if self.total_score and self.course_handicap:
            return self.total_score - self.course_handicap
        return None

    def calculate_differential(self):
        """Calculate handicap differential"""
        if self.total_score and self.course_rating and self.slope_rating:
            return round((self.total_score - self.course_rating) * 113 / self.slope_rating, 1)
        return None

    def calculate_course_handicap(self, handicap_index=None):
        """Calculate course handicap from handicap index"""
        if not handicap_index:
            handicap_index = self.handicap_used
            
        if handicap_index and self.slope_rating:
            return round(handicap_index * self.slope_rating / 113)
        return None

    def stamp_ratings_from_tee_set(self):
        """Stamp course and slope ratings from the tee set"""
        if self.tee_set and self.user:
            ratings = self.tee_set.get_rating_for_gender(self.user.sex)
            self.course_rating = ratings['course_rating']
            self.slope_rating = ratings['slope_rating']

    def calculate_totals(self):
        """Calculate total score and points from individual hole scores"""
        if self.scores:
            self.total_score = sum(score.strokes for score in self.scores if score.strokes)
            self.total_points = sum(score.points for score in self.scores if score.points)
            self.differential = self.calculate_differential()

    def to_dict(self, include_scores=False):
        """Convert model to dictionary for JSON serialization"""
        data = {
            'id': self.id,
            'date_played': self.date_played.isoformat() if self.date_played else None,
            'handicap_used': self.handicap_used,
            'course_handicap': self.course_handicap,
            'course_rating': self.course_rating,
            'slope_rating': self.slope_rating,
            'total_score': self.total_score,
            'total_points': self.total_points,
            'net_score': self.net_score,
            'differential': self.differential,
            'is_complete': self.is_complete,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'tee_set_id': self.tee_set_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_scores:
            data['scores'] = [score.to_dict() for score in self.scores]
            
        return data