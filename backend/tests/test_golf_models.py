"""
Golf-specific model tests for Course, Hole, TeeSet, TeePosition, Round, Score functionality
"""
import pytest
from datetime import datetime, date
from app.models.course import Course
from app.models.hole import Hole
from app.models.tee_set import TeeSet
from app.models.tee_position import TeePosition
from app.models.round import Round
from app.models.score import Score
from app.models.user import User
from app.models.club import Club
from app.extensions import db


class TestCourseModel:
    """Test Course model functionality"""
    
    def test_course_creation(self, app, test_club):
        """Test creating a new golf course"""
        with app.app_context():
            # Merge test_club into current session
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Pine Valley Golf Course',
                holes_count=18,
                description='Championship golf course',
                club_id=club.id
            )
            db.session.add(course)
            db.session.commit()
            
            assert course.name == 'Pine Valley Golf Course'
            assert course.holes_count == 18
            assert course.description == 'Championship golf course'
            assert course.club_id == club.id
    
    def test_course_club_relationship(self, app, test_club):
        """Test course-club relationship"""
        with app.app_context():
            # Merge test_club into current session
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            # Test relationship from course side
            assert course.club.name == club.name
            
            # Test relationship from club side
            assert course in club.courses
    
    def test_course_total_par_property(self, app, test_club):
        """Test total par calculation property"""
        with app.app_context():
            # Merge test_club into current session
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            # Add some holes with different pars
            holes_data = [
                (1, 4), (2, 3), (3, 5), (4, 4), (5, 4), (6, 3), 
                (7, 4), (8, 5), (9, 4), (10, 4), (11, 3), (12, 4),
                (13, 5), (14, 4), (15, 4), (16, 3), (17, 4), (18, 5)
            ]
            
            for hole_num, par in holes_data:
                hole = Hole(
                    course_id=course.id,
                    hole_number=hole_num,
                    par=par,
                    stroke_index=hole_num
                )
                db.session.add(hole)
            
            db.session.commit()
            
            # Test total par calculation (should be 72)
            expected_par = sum(par for _, par in holes_data)
            assert course.total_par == expected_par
            assert course.total_par == 72
    
    def test_course_to_dict(self, app, test_club):
        """Test course serialization"""
        with app.app_context():
            # Merge test_club into current session
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18,
                description='Test course description'
            )
            db.session.add(course)
            db.session.commit()
            
            # Test basic serialization
            data = course.to_dict()
            assert data['name'] == 'Test Course'
            assert data['holes_count'] == 18
            assert data['club_id'] == club.id
            assert 'created_at' in data
            assert 'updated_at' in data


class TestHoleModel:
    """Test Hole model functionality"""
    
    def test_hole_creation(self, app, test_club):
        """Test creating a golf hole"""
        with app.app_context():
            # Merge test_club into current session
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            hole = Hole(
                course_id=course.id,
                hole_number=1,
                par=4,
                stroke_index=10
            )
            db.session.add(hole)
            db.session.commit()
            
            assert hole.hole_number == 1
            assert hole.par == 4
            assert hole.stroke_index == 10
            assert hole.course_id == course.id
    
    def test_hole_course_relationship(self, app, test_club):
        """Test hole-course relationship"""
        with app.app_context():
            # Merge test_club into current session
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            hole = Hole(
                course_id=course.id,
                hole_number=1,
                par=4,
                stroke_index=1
            )
            db.session.add(hole)
            db.session.commit()
            
            # Test relationship
            assert hole.course.name == 'Test Course'
            assert hole in course.holes
    
    def test_hole_unique_constraint(self, app, test_club):
        """Test unique constraint on hole number per course"""
        with app.app_context():
            # Merge test_club into current session
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            hole1 = Hole(
                course_id=course.id,
                hole_number=1,
                par=4,
                stroke_index=1
            )
            
            db.session.add(hole1)
            db.session.commit()
            
            hole2 = Hole(
                course_id=course.id,
                hole_number=1,  # Same hole number
                par=3,
                stroke_index=2
            )
            
            db.session.add(hole2)
            with pytest.raises(Exception):  # Should raise IntegrityError
                db.session.commit()
    
    def test_hole_to_dict(self, app, test_club):
        """Test hole serialization"""
        with app.app_context():
            # Merge test_club into current session
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            hole = Hole(
                course_id=course.id,
                hole_number=1,
                par=4,
                stroke_index=5
            )
            db.session.add(hole)
            db.session.commit()
            
            data = hole.to_dict()
            assert data['hole_number'] == 1
            assert data['par'] == 4
            assert data['stroke_index'] == 5
            assert data['course_id'] == course.id


class TestTeeSetModel:
    """Test TeeSet model functionality"""
    
    def test_tee_set_creation(self, app, test_club):
        """Test creating a tee set"""
        with app.app_context():
            # Merge test_club into current session
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            tee_set = TeeSet(
                course_id=course.id,
                name='Championship Tees',
                slope_rating=142.0,
                course_rating=74.2,
                women_slope_rating=138.0,
                women_course_rating=71.8
            )
            db.session.add(tee_set)
            db.session.commit()
            
            assert tee_set.name == 'Championship Tees'
            assert tee_set.slope_rating == 142.0
            assert tee_set.course_rating == 74.2
            assert tee_set.women_slope_rating == 138.0
            assert tee_set.women_course_rating == 71.8
    
    def test_tee_set_course_relationship(self, app, test_club):
        """Test tee set-course relationship"""
        with app.app_context():
            # Merge test_club into current session
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            tee_set = TeeSet(
                course_id=course.id,
                name='Regular Tees',
                slope_rating=113.0,
                course_rating=72.0
            )
            db.session.add(tee_set)
            db.session.commit()
            
            # Test relationship
            assert tee_set.course.name == 'Test Course'
            assert tee_set in course.tee_sets
    
    def test_get_rating_for_gender(self, app, test_club):
        """Test gender-specific rating retrieval"""
        with app.app_context():
            # Merge test_club into current session
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            tee_set = TeeSet(
                course_id=course.id,
                name='Championship Tees',
                slope_rating=142.0,
                course_rating=74.2,
                women_slope_rating=138.0,
                women_course_rating=71.8
            )
            db.session.add(tee_set)
            db.session.commit()
            
            # Test men's ratings (default)
            men_ratings = tee_set.get_rating_for_gender('M')
            assert men_ratings['course_rating'] == 74.2
            assert men_ratings['slope_rating'] == 142.0
            
            # Test women's ratings
            women_ratings = tee_set.get_rating_for_gender('F')
            assert women_ratings['course_rating'] == 71.8
            assert women_ratings['slope_rating'] == 138.0
    
    def test_get_rating_fallback_to_mens(self, app, test_club):
        """Test fallback to men's ratings when women's not available"""
        with app.app_context():
            # Merge test_club into current session
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            tee_set = TeeSet(
                course_id=course.id,
                name='Regular Tees',
                slope_rating=113.0,
                course_rating=72.0
                # No women's ratings
            )
            db.session.add(tee_set)
            db.session.commit()
            
            # Should fallback to men's ratings
            women_ratings = tee_set.get_rating_for_gender('F')
            assert women_ratings['course_rating'] == 72.0
            assert women_ratings['slope_rating'] == 113.0


class TestTeePositionModel:
    """Test TeePosition model functionality"""
    
    def test_tee_position_creation(self, app, test_club):
        """Test creating a tee position"""
        with app.app_context():
            # Merge test_club into current session
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            hole = Hole(
                course_id=course.id,
                hole_number=1,
                par=4,
                stroke_index=1
            )
            tee_set = TeeSet(
                course_id=course.id,
                name='Regular Tees',
                slope_rating=113.0,
                course_rating=72.0
            )
            db.session.add_all([hole, tee_set])
            db.session.commit()
            
            tee_position = TeePosition(
                hole_id=hole.id,
                tee_set_id=tee_set.id,
                length=384  # meters
            )
            db.session.add(tee_position)
            db.session.commit()
            
            assert tee_position.length == 384
            assert tee_position.hole_id == hole.id
            assert tee_position.tee_set_id == tee_set.id
    
    def test_tee_position_relationships(self, app, test_club):
        """Test tee position relationships with hole and tee set"""
        with app.app_context():
            # Merge test_club into current session
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            hole = Hole(
                course_id=course.id,
                hole_number=1,
                par=4,
                stroke_index=1
            )
            tee_set = TeeSet(
                course_id=course.id,
                name='Regular Tees',
                slope_rating=113.0,
                course_rating=72.0
            )
            db.session.add_all([hole, tee_set])
            db.session.commit()
            
            tee_position = TeePosition(
                hole_id=hole.id,
                tee_set_id=tee_set.id,
                length=384
            )
            db.session.add(tee_position)
            db.session.commit()
            
            # Test relationships
            assert tee_position.hole.hole_number == 1
            assert tee_position.tee_set.name == 'Regular Tees'
            assert tee_position in hole.tee_positions
            assert tee_position in tee_set.tee_positions
    
    def test_tee_position_unique_constraint(self, app, test_club):
        """Test unique constraint on hole-teeset combination"""
        with app.app_context():
            # Merge test_club into current session
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            hole = Hole(
                course_id=course.id,
                hole_number=1,
                par=4,
                stroke_index=1
            )
            tee_set = TeeSet(
                course_id=course.id,
                name='Regular Tees',
                slope_rating=113.0,
                course_rating=72.0
            )
            db.session.add_all([hole, tee_set])
            db.session.commit()
            
            tee_pos1 = TeePosition(
                hole_id=hole.id,
                tee_set_id=tee_set.id,
                length=384
            )
            db.session.add(tee_pos1)
            db.session.commit()
            
            tee_pos2 = TeePosition(
                hole_id=hole.id,
                tee_set_id=tee_set.id,  # Same combination
                length=400
            )
            
            db.session.add(tee_pos2)
            with pytest.raises(Exception):  # Should raise IntegrityError
                db.session.commit()
    
    def test_length_conversion_methods(self, app, test_club):
        """Test length conversion between meters and yards"""
        with app.app_context():
            # Merge test_club into current session
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            hole = Hole(
                course_id=course.id,
                hole_number=1,
                par=4,
                stroke_index=1
            )
            tee_set = TeeSet(
                course_id=course.id,
                name='Regular Tees',
                slope_rating=113.0,
                course_rating=72.0
            )
            db.session.add_all([hole, tee_set])
            db.session.commit()
            
            tee_position = TeePosition(
                hole_id=hole.id,
                tee_set_id=tee_set.id,
                length=384  # meters
            )
            db.session.add(tee_position)
            db.session.commit()
            
            # Test conversion to yards
            yards = tee_position.length_in_yards()
            expected_yards = round(384 * 1.09361, 1)
            assert yards == expected_yards
            
            # Test get_length_in_unit method
            assert tee_position.get_length_in_unit('meters') == 384
            assert tee_position.get_length_in_unit('yards') == expected_yards


class TestRoundModel:
    """Test Round model functionality"""
    
    def test_round_creation(self, app, test_user, test_club):
        """Test creating a golf round"""
        with app.app_context():
            # Merge instances into current session
            user = db.session.merge(test_user)
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            tee_set = TeeSet(
                course_id=course.id,
                name='Regular Tees',
                slope_rating=113.0,
                course_rating=72.0
            )
            db.session.add(tee_set)
            db.session.commit()
            
            round_obj = Round(
                user_id=user.id,
                course_id=course.id,
                tee_set_id=tee_set.id,
                date_played=date.today(),
                total_score=85,
                handicap_used=18.5,
                course_handicap=20
            )
            db.session.add(round_obj)
            db.session.commit()
            
            assert round_obj.user_id == user.id
            assert round_obj.course_id == course.id
            assert round_obj.tee_set_id == tee_set.id
            assert round_obj.total_score == 85
            assert round_obj.handicap_used == 18.5
            assert round_obj.course_handicap == 20
            assert round_obj.date_played == date.today()
    
    def test_round_relationships(self, app, test_user, test_club):
        """Test round relationships with user, course, and tee set"""
        with app.app_context():
            # Merge instances into current session
            user = db.session.merge(test_user)
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            tee_set = TeeSet(
                course_id=course.id,
                name='Regular Tees',
                slope_rating=113.0,
                course_rating=72.0
            )
            db.session.add(tee_set)
            db.session.commit()
            
            round_obj = Round(
                user_id=user.id,
                course_id=course.id,
                tee_set_id=tee_set.id,
                date_played=date.today(),
                total_score=85
            )
            db.session.add(round_obj)
            db.session.commit()
            
            # Test relationships
            assert round_obj.user.email == user.email
            assert round_obj.course.name == 'Test Course'
            assert round_obj.tee_set.name == 'Regular Tees'
            assert round_obj in user.rounds
    
    def test_round_net_score_calculation(self, app, test_user, test_club):
        """Test net score calculation"""
        with app.app_context():
            # Merge instances into current session
            user = db.session.merge(test_user)
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            tee_set = TeeSet(
                course_id=course.id,
                name='Regular Tees',
                slope_rating=113.0,
                course_rating=72.0
            )
            db.session.add(tee_set)
            db.session.commit()
            
            round_obj = Round(
                user_id=user.id,
                course_id=course.id,
                tee_set_id=tee_set.id,
                date_played=date.today(),
                total_score=85,
                course_handicap=12
            )
            db.session.add(round_obj)
            db.session.commit()
            
            # Net score = gross score - course handicap
            assert round_obj.net_score == 73  # 85 - 12
    
    def test_round_differential_calculation(self, app, test_user, test_club):
        """Test handicap differential calculation"""
        with app.app_context():
            # Merge instances into current session
            user = db.session.merge(test_user)
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            tee_set = TeeSet(
                course_id=course.id,
                name='Regular Tees',
                slope_rating=113.0,
                course_rating=72.0
            )
            db.session.add(tee_set)
            db.session.commit()
            
            round_obj = Round(
                user_id=user.id,
                course_id=course.id,
                tee_set_id=tee_set.id,
                date_played=date.today(),
                total_score=85,
                course_rating=72.0,
                slope_rating=113.0
            )
            db.session.add(round_obj)
            db.session.commit()
            
            # Differential = (Score - Course Rating) * 113 / Slope Rating
            expected_diff = round((85 - 72.0) * 113 / 113.0, 1)
            assert round_obj.calculate_differential() == expected_diff
            assert round_obj.calculate_differential() == 13.0
    
    def test_round_course_handicap_calculation(self, app, test_user, test_club):
        """Test course handicap calculation"""
        with app.app_context():
            # Merge instances into current session
            user = db.session.merge(test_user)
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            tee_set = TeeSet(
                course_id=course.id,
                name='Regular Tees',
                slope_rating=142.0,
                course_rating=74.2
            )
            db.session.add(tee_set)
            db.session.commit()
            
            round_obj = Round(
                user_id=user.id,
                course_id=course.id,
                tee_set_id=tee_set.id,
                date_played=date.today(),
                slope_rating=142.0
            )
            db.session.add(round_obj)
            db.session.commit()
            
            # Course Handicap = Handicap Index * Slope Rating / 113
            handicap_index = 18.0
            expected_course_hcp = round(handicap_index * 142.0 / 113)
            assert round_obj.calculate_course_handicap(handicap_index) == expected_course_hcp
            assert round_obj.calculate_course_handicap(handicap_index) == 23


class TestScoreModel:
    """Test Score model functionality"""
    
    def test_score_creation(self, app, test_user, test_club):
        """Test creating a score for a hole"""
        with app.app_context():
            # Merge instances into current session
            user = db.session.merge(test_user)
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            hole = Hole(
                course_id=course.id,
                hole_number=1,
                par=4,
                stroke_index=1
            )
            tee_set = TeeSet(
                course_id=course.id,
                name='Regular Tees',
                slope_rating=113.0,
                course_rating=72.0
            )
            db.session.add_all([hole, tee_set])
            db.session.commit()
            
            round_obj = Round(
                user_id=user.id,
                course_id=course.id,
                tee_set_id=tee_set.id,
                date_played=date.today()
            )
            db.session.add(round_obj)
            db.session.commit()
            
            score = Score(
                round_id=round_obj.id,
                hole_id=hole.id,
                strokes=5,
                points=1  # Stableford points
            )
            db.session.add(score)
            db.session.commit()
            
            assert score.round_id == round_obj.id
            assert score.hole_id == hole.id
            assert score.strokes == 5
            assert score.points == 1
    
    def test_score_relationships(self, app, test_user, test_club):
        """Test score relationships with round and hole"""
        with app.app_context():
            # Merge instances into current session
            user = db.session.merge(test_user)
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            hole = Hole(
                course_id=course.id,
                hole_number=1,
                par=4,
                stroke_index=1
            )
            tee_set = TeeSet(
                course_id=course.id,
                name='Regular Tees',
                slope_rating=113.0,
                course_rating=72.0
            )
            db.session.add_all([hole, tee_set])
            db.session.commit()
            
            round_obj = Round(
                user_id=user.id,
                course_id=course.id,
                tee_set_id=tee_set.id,
                date_played=date.today()
            )
            db.session.add(round_obj)
            db.session.commit()
            
            score = Score(
                round_id=round_obj.id,
                hole_id=hole.id,
                strokes=5,
                points=1
            )
            db.session.add(score)
            db.session.commit()
            
            # Test relationships
            assert score.round.user.email == user.email
            assert score.hole.hole_number == 1
            assert score in round_obj.scores
    
    def test_score_to_par_property(self, app, test_user, test_club):
        """Test score to par calculation"""
        with app.app_context():
            # Merge instances into current session
            user = db.session.merge(test_user)
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            hole = Hole(
                course_id=course.id,
                hole_number=1,
                par=4,
                stroke_index=1
            )
            tee_set = TeeSet(
                course_id=course.id,
                name='Regular Tees',
                slope_rating=113.0,
                course_rating=72.0
            )
            db.session.add_all([hole, tee_set])
            db.session.commit()
            
            round_obj = Round(
                user_id=user.id,
                course_id=course.id,
                tee_set_id=tee_set.id,
                date_played=date.today()
            )
            db.session.add(round_obj)
            db.session.commit()
            
            # Test different scores relative to par
            birdie_score = Score(
                round_id=round_obj.id,
                hole_id=hole.id,
                strokes=3  # One under par
            )
            db.session.add(birdie_score)
            db.session.commit()
            
            assert birdie_score.score_to_par == "-1"
            
            # Test par score
            db.session.delete(birdie_score)
            par_score = Score(
                round_id=round_obj.id,
                hole_id=hole.id,
                strokes=4  # Even with par
            )
            db.session.add(par_score)
            db.session.commit()
            
            assert par_score.score_to_par == "E"
            
            # Test bogey score
            db.session.delete(par_score)
            bogey_score = Score(
                round_id=round_obj.id,
                hole_id=hole.id,
                strokes=5  # One over par
            )
            db.session.add(bogey_score)
            db.session.commit()
            
            assert bogey_score.score_to_par == "+1"
    
    def test_score_name_property(self, app, test_user, test_club):
        """Test traditional golf score names"""
        with app.app_context():
            # Merge instances into current session
            user = db.session.merge(test_user)
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            hole = Hole(
                course_id=course.id,
                hole_number=1,
                par=4,
                stroke_index=1
            )
            tee_set = TeeSet(
                course_id=course.id,
                name='Regular Tees',
                slope_rating=113.0,
                course_rating=72.0
            )
            db.session.add_all([hole, tee_set])
            db.session.commit()
            
            round_obj = Round(
                user_id=user.id,
                course_id=course.id,
                tee_set_id=tee_set.id,
                date_played=date.today()
            )
            db.session.add(round_obj)
            db.session.commit()
            
            # Test score names
            test_cases = [
                (1, "Albatross"),  # 3 under par
                (2, "Eagle"),      # 2 under par
                (3, "Birdie"),     # 1 under par
                (4, "Par"),        # Even with par
                (5, "Bogey"),      # 1 over par
                (6, "Double Bogey"), # 2 over par
                (7, "Triple Bogey"), # 3 over par
                (8, "4-over par")    # 4+ over par
            ]
            
            for strokes, expected_name in test_cases:
                score = Score(
                    round_id=round_obj.id,
                    hole_id=hole.id,
                    strokes=strokes
                )
                db.session.add(score)
                db.session.commit()
                
                assert score.score_name == expected_name
                
                db.session.delete(score)
                db.session.commit()
    
    def test_stableford_points_calculation(self, app, test_user, test_club):
        """Test Stableford points calculation"""
        with app.app_context():
            # Merge instances into current session
            user = db.session.merge(test_user)
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            tee_set = TeeSet(
                course_id=course.id,
                name='Regular Tees',
                slope_rating=113.0,
                course_rating=72.0
            )
            db.session.add(tee_set)
            db.session.commit()
            
            round_obj = Round(
                user_id=user.id,
                course_id=course.id,
                tee_set_id=tee_set.id,
                date_played=date.today()
            )
            db.session.add(round_obj)
            db.session.commit()
            
            # Test Stableford points for different scores
            # With course handicap of 18 (1 stroke per hole)
            # On hole with stroke index 1, player gets 1 stroke
            # Net strokes = actual strokes - 1
            course_handicap = 18
            
            test_cases = [
                # (actual_strokes, expected_points)
                # Net strokes calculation: actual - 1 stroke received
                (1, 5),  # Net 0 (4 under par) = 5 points (albatross or better)
                (2, 5),  # Net 1 (3 under par) = 5 points (albatross or better)
                (3, 4),  # Net 2 (2 under par) = 4 points (eagle)
                (4, 3),  # Net 3 (1 under par) = 3 points (birdie)
                (5, 2),  # Net 4 (even par) = 2 points (par)
                (6, 1),  # Net 5 (1 over par) = 1 point (bogey)
                (7, 0),  # Net 6 (2 over par) = 0 points (double bogey)
            ]
            
            for i, (strokes, expected_points) in enumerate(test_cases):
                # Create a separate hole for each test case to avoid unique constraint
                hole = Hole(
                    course_id=course.id,
                    hole_number=i + 1,  # Different hole numbers
                    par=4,
                    stroke_index=1  # Low stroke index = hard hole
                )
                db.session.add(hole)
                db.session.flush()  # Get the hole ID
                
                score = Score(
                    round_id=round_obj.id,
                    hole_id=hole.id,
                    strokes=strokes
                )
                
                # Add to session so relationships are loaded
                db.session.add(score)
                db.session.flush()  # Flush to establish relationships without committing
                
                calculated_points = score.calculate_stableford_points(course_handicap)
                assert calculated_points == expected_points, f"Strokes {strokes}: expected {expected_points}, got {calculated_points}"
                
                # Test the update method
                score.update_stableford_points(course_handicap)
                assert score.points == expected_points
    
    def test_score_unique_constraint(self, app, test_user, test_club):
        """Test unique constraint on round-hole combination"""
        with app.app_context():
            # Merge instances into current session
            user = db.session.merge(test_user)
            club = db.session.merge(test_club)
            db.session.commit()
            
            course = Course(
                name='Test Course',
                club_id=club.id,
                holes_count=18
            )
            db.session.add(course)
            db.session.commit()
            
            hole = Hole(
                course_id=course.id,
                hole_number=1,
                par=4,
                stroke_index=1
            )
            tee_set = TeeSet(
                course_id=course.id,
                name='Regular Tees',
                slope_rating=113.0,
                course_rating=72.0
            )
            db.session.add_all([hole, tee_set])
            db.session.commit()
            
            round_obj = Round(
                user_id=user.id,
                course_id=course.id,
                tee_set_id=tee_set.id,
                date_played=date.today()
            )
            db.session.add(round_obj)
            db.session.commit()
            
            score1 = Score(
                round_id=round_obj.id,
                hole_id=hole.id,
                strokes=4
            )
            db.session.add(score1)
            db.session.commit()
            
            score2 = Score(
                round_id=round_obj.id,
                hole_id=hole.id,  # Same round and hole
                strokes=5
            )
            
            db.session.add(score2)
            with pytest.raises(Exception):  # Should raise IntegrityError
                db.session.commit() 