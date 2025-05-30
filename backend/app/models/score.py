from datetime import datetime
from app.extensions import db

class Score(db.Model):
    """
    Score Model
    
    Represents the score for a single hole within a round.
    Contains strokes and Stableford points for that hole.
    """
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    strokes = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=True)  # Stableford points
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    round_id = db.Column(db.Integer, db.ForeignKey('rounds.id'), nullable=False)
    hole_id = db.Column(db.Integer, db.ForeignKey('holes.id'), nullable=False)

    # Relationships
    round = db.relationship('Round', back_populates='scores')
    hole = db.relationship('Hole', back_populates='scores')

    # Unique constraint to prevent duplicate scores per hole per round
    __table_args__ = (
        db.UniqueConstraint('round_id', 'hole_id', name='unique_score_per_hole'),
    )

    def __repr__(self):
        return f'<Score Hole {self.hole.hole_number if self.hole else "?"} - {self.strokes} strokes>'

    @property
    def score_to_par(self):
        """Calculate score relative to par (e.g., +1, -2, E)"""
        if self.hole and self.hole.par:
            diff = self.strokes - self.hole.par
            if diff == 0:
                return "E"
            elif diff > 0:
                return f"+{diff}"
            else:
                return str(diff)
        return None

    @property
    def score_name(self):
        """Get traditional golf score name (e.g., eagle, birdie, par, etc.)"""
        if not self.hole or not self.hole.par:
            return None
            
        diff = self.strokes - self.hole.par
        score_names = {
            -4: "Condor",
            -3: "Albatross", 
            -2: "Eagle",
            -1: "Birdie",
            0: "Par",
            1: "Bogey",
            2: "Double Bogey",
            3: "Triple Bogey"
        }
        
        if diff in score_names:
            return score_names[diff]
        elif diff > 3:
            return f"{diff}-over par"
        else:
            return f"{abs(diff)}-under par"

    def calculate_stableford_points(self, course_handicap=0):
        """
        Calculate Stableford points for this hole.
        
        Args:
            course_handicap: Player's course handicap for stroke allocation
        """
        if not self.hole:
            return 0
            
        # Calculate strokes received on this hole
        strokes_received = 0
        if course_handicap > 0:
            if course_handicap >= self.hole.stroke_index:
                strokes_received = 1
            if course_handicap >= self.hole.stroke_index + 18:
                strokes_received = 2
                
        # Net strokes = actual strokes - strokes received
        net_strokes = self.strokes - strokes_received
        par = self.hole.par
        
        # Stableford scoring (correct points)
        if net_strokes <= par - 3:
            return 5  # Albatross or better (3+ under par)
        elif net_strokes == par - 2:
            return 4  # Eagle (2 under par)
        elif net_strokes == par - 1:
            return 3  # Birdie (1 under par)
        elif net_strokes == par:
            return 2  # Par (even with par)
        elif net_strokes == par + 1:
            return 1  # Bogey (1 over par)
        else:
            return 0  # Double bogey or worse

    def update_stableford_points(self, course_handicap=0):
        """Update the points field with calculated Stableford points"""
        self.points = self.calculate_stableford_points(course_handicap)

    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'strokes': self.strokes,
            'points': self.points,
            'score_to_par': self.score_to_par,
            'score_name': self.score_name,
            'round_id': self.round_id,
            'hole_id': self.hole_id,
            'hole_number': self.hole.hole_number if self.hole else None,
            'hole_par': self.hole.par if self.hole else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

