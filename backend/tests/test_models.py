"""
Model tests for User and related models
"""
import pytest
from datetime import datetime, timedelta
from app.models.user import User
from app.models.club import Club
from app.models.theme import Theme
from app.models.handicap import Handicap
from app.extensions import db


class TestUserModel:
    """Test User model functionality"""
    
    def test_user_creation(self, app):
        """Test creating a new user"""
        with app.app_context():
            user = User(
                email='test@example.com',
                first_name='Test',
                last_name='User',
                sex='M',
                is_active=True,  # Explicitly set
                is_admin=False   # Explicitly set
            )
            user.set_password('testpass123')
            db.session.add(user)
            db.session.commit()
            
            assert user.email == 'test@example.com'
            assert user.first_name == 'Test'
            assert user.last_name == 'User'
            assert user.sex == 'M'
            assert user.is_active is True
            assert user.is_admin is False
            assert user.distance_unit == 'meters'  # Default value
            assert user.timezone == 'Europe/Oslo'  # Default value
    
    def test_password_hashing(self, app):
        """Test password hashing and verification"""
        with app.app_context():
            user = User(
                email='test@example.com',
                first_name='Test',
                last_name='User',
                sex='M'
            )
            user.set_password('testpass123')
            
            # Password should be hashed, not stored in plain text
            assert user.password_hash != 'testpass123'
            assert user.password_hash is not None
            
            # Should be able to verify correct password
            assert user.check_password('testpass123') is True
            
            # Should reject incorrect password
            assert user.check_password('wrongpassword') is False
    
    def test_full_name_property(self, app):
        """Test full_name property"""
        with app.app_context():
            user = User(
                email='test@example.com',
                first_name='John',
                last_name='Doe',
                sex='M'
            )
            
            assert user.full_name == 'John Doe'
    
    def test_full_address_property(self, app):
        """Test full_address property"""
        with app.app_context():
            user = User(
                email='test@example.com',
                first_name='Test',
                last_name='User',
                sex='M',
                address='123 Golf Street',
                city='Golf City',
                postal_code='12345',
                country='Norway'
            )
            
            expected_address = '123 Golf Street, Golf City, 12345, Norway'
            assert user.full_address == expected_address
    
    def test_full_address_partial(self, app):
        """Test full_address property with partial data"""
        with app.app_context():
            user = User(
                email='test@example.com',
                first_name='Test',
                last_name='User',
                sex='M',
                city='Golf City',
                country='Norway'
                # Missing address and postal_code
            )
            
            expected_address = 'Golf City, Norway'
            assert user.full_address == expected_address
    
    def test_to_dict_basic(self, app):
        """Test to_dict method without sensitive data"""
        with app.app_context():
            user = User(
                email='test@example.com',
                first_name='Test',
                last_name='User',
                sex='F',
                city='Test City',
                country='Test Country'
            )
            user.set_password('testpass123')
            db.session.add(user)
            db.session.commit()
            
            data = user.to_dict()
            
            # Should include basic user data
            assert data['email'] == 'test@example.com'
            assert data['first_name'] == 'Test'
            assert data['last_name'] == 'User'
            assert data['full_name'] == 'Test User'
            assert data['sex'] == 'F'
            assert data['is_active'] is True
            
            # Should not include sensitive data by default
            assert 'is_admin' not in data
            assert 'password_reset_token' not in data
    
    def test_to_dict_with_sensitive(self, app):
        """Test to_dict method with sensitive data"""
        with app.app_context():
            user = User(
                email='admin@example.com',
                first_name='Admin',
                last_name='User',
                sex='M',
                is_admin=True
            )
            user.set_password('adminpass123')
            db.session.add(user)
            db.session.commit()
            
            data = user.to_dict(include_sensitive=True)
            
            # Should include sensitive data when requested
            assert data['is_admin'] is True
            assert 'password_reset_token' in data
            assert 'password_reset_expires' in data
    
    def test_user_club_relationship(self, app):
        """Test user-club relationship"""
        with app.app_context():
            # Create club first
            club = Club(
                name='Test Golf Club',
                description='A test golf club',
                city='Test City',
                country='Test Country',
                timezone='Europe/Oslo'
            )
            db.session.add(club)
            db.session.commit()
            
            user = User(
                email='test@example.com',
                first_name='Test',
                last_name='User',
                sex='M',
                home_club_id=club.id
            )
            user.set_password('testpass123')
            db.session.add(user)
            db.session.commit()
            
            # Test relationship from user side
            assert user.home_club.name == 'Test Golf Club'
            
            # Test relationship from club side
            assert user in club.members
    
    def test_user_theme_relationship(self, app):
        """Test user-theme relationship"""
        with app.app_context():
            # Create theme first
            theme = Theme(
                name='Test Theme',
                description='A test theme'
            )
            db.session.add(theme)
            db.session.commit()
            
            user = User(
                email='test@example.com',
                first_name='Test',
                last_name='User',
                sex='M',
                preferred_theme_id=theme.id
            )
            user.set_password('testpass123')
            db.session.add(user)
            db.session.commit()
            
            # Test relationship from user side
            assert user.preferred_theme.name == 'Test Theme'
            
            # Test relationship from theme side
            assert user in theme.users
    
    def test_current_handicap_property(self, app):
        """Test current_handicap property"""
        with app.app_context():
            user = User(
                email='test@example.com',
                first_name='Test',
                last_name='User',
                sex='M'
            )
            user.set_password('testpass123')
            db.session.add(user)
            db.session.commit()
            
            # No current handicap initially
            assert user.current_handicap is None
            
            # Add a current handicap (no end date)
            handicap = Handicap(
                handicap_value=18.5,
                start_date=datetime.utcnow().date(),
                user_id=user.id,
                created_by_id=user.id
            )
            db.session.add(handicap)
            db.session.commit()
            
            # Should return current handicap value
            assert user.current_handicap == 18.5
    
    def test_user_handicaps_relationship(self, app):
        """Test user handicaps relationship with foreign key specification"""
        with app.app_context():
            # Create users
            user = User(
                email='player@example.com',
                first_name='Player',
                last_name='User',
                sex='M'
            )
            user.set_password('playerpass123')
            admin = User(
                email='admin@example.com',
                first_name='Admin',
                last_name='User',
                sex='F',
                is_admin=True
            )
            admin.set_password('adminpass123')
            db.session.add_all([user, admin])
            db.session.commit()
            
            # Create handicap where admin creates handicap for player
            handicap = Handicap(
                handicap_value=15.2,
                start_date=datetime.utcnow().date(),
                user_id=user.id,
                created_by_id=admin.id
            )
            db.session.add(handicap)
            db.session.commit()
            
            # Test user.handicaps relationship (user_id foreign key)
            assert len(user.handicaps) == 1
            assert user.handicaps[0].handicap_value == 15.2
            
            # Test admin.created_handicaps relationship (created_by_id foreign key)
            assert len(admin.created_handicaps) == 1
            assert admin.created_handicaps[0].handicap_value == 15.2
            
            # Test backref relationships
            assert handicap.user == user
            assert handicap.created_by == admin


class TestClubModel:
    """Test Club model functionality"""
    
    def test_club_creation(self, app):
        """Test creating a new club"""
        with app.app_context():
            club = Club(
                name='Test Golf Club',
                description='A great golf club',
                city='Test City',
                country='Norway',
                timezone='Europe/Oslo'
            )
            
            assert club.name == 'Test Golf Club'
            assert club.description == 'A great golf club'
            assert club.city == 'Test City'
            assert club.country == 'Norway'
            assert club.timezone == 'Europe/Oslo'
    
    def test_club_unique_name(self, app):
        """Test club name uniqueness constraint"""
        with app.app_context():
            club1 = Club(
                name='Unique Club',
                city='City1',
                country='Country1',
                timezone='Europe/Oslo'
            )
            club2 = Club(
                name='Unique Club',  # Same name
                city='City2',
                country='Country2',
                timezone='Europe/Oslo'
            )
            
            db.session.add(club1)
            db.session.commit()
            
            db.session.add(club2)
            with pytest.raises(Exception):  # Should raise IntegrityError
                db.session.commit()


class TestThemeModel:
    """Test Theme model functionality"""
    
    def test_theme_creation(self, app):
        """Test creating a new theme"""
        with app.app_context():
            theme = Theme(
                name='Dark Theme',
                description='A dark color scheme'
            )
            
            assert theme.name == 'Dark Theme'
            assert theme.description == 'A dark color scheme'
    
    def test_theme_unique_name(self, app):
        """Test theme name uniqueness constraint"""
        with app.app_context():
            theme1 = Theme(name='Unique Theme')
            theme2 = Theme(name='Unique Theme')  # Same name
            
            db.session.add(theme1)
            db.session.commit()
            
            db.session.add(theme2)
            with pytest.raises(Exception):  # Should raise IntegrityError
                db.session.commit() 