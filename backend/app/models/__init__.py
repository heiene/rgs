"""
Models package initialization

Import all models here to ensure SQLAlchemy relationships work properly.
"""

# Import all models to register them with SQLAlchemy
from .user import User
from .club import Club
from .theme import Theme
from .course import Course
from .hole import Hole
from .tee_set import TeeSet
from .tee_position import TeePosition
from .round import Round
from .score import Score
from .handicap import Handicap

# Make models available when importing from this package
__all__ = [
    'User',
    'Club', 
    'Theme',
    'Course',
    'Hole',
    'TeeSet',
    'TeePosition',
    'Round',
    'Score',
    'Handicap'
] 