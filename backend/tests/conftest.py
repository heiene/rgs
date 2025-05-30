"""
Pytest configuration and fixtures
"""
import pytest
from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.club import Club
from app.models.theme import Theme


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def test_user(app):
    """Create a test user"""
    with app.app_context():
        user = User(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            sex='M',
            is_active=True,
            is_admin=False
        )
        user.set_password('testpass123')
        db.session.add(user)
        db.session.commit()
        
        # Refresh to avoid detached instance issues
        db.session.refresh(user)
        return user


@pytest.fixture
def admin_user(app):
    """Create an admin test user"""
    with app.app_context():
        user = User(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            sex='F',
            is_active=True,
            is_admin=True
        )
        user.set_password('adminpass123')
        db.session.add(user)
        db.session.commit()
        
        # Refresh to avoid detached instance issues
        db.session.refresh(user)
        return user


@pytest.fixture
def test_club(app):
    """Create a test club"""
    with app.app_context():
        club = Club(
            name='Test Golf Club',
            description='A test golf club',
            city='Test City',
            country='Test Country',
            timezone='Europe/Oslo'
        )
        db.session.add(club)
        db.session.commit()
        
        # Refresh to avoid detached instance issues
        db.session.refresh(club)
        return club


@pytest.fixture
def test_theme(app):
    """Create a test theme"""
    with app.app_context():
        theme = Theme(
            name='Test Theme',
            description='A test theme'
        )
        db.session.add(theme)
        db.session.commit()
        
        # Refresh to avoid detached instance issues
        db.session.refresh(theme)
        return theme


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for test user"""
    response = client.post('/api/v1/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    data = response.get_json()
    token = data['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def admin_headers(client, admin_user):
    """Get authentication headers for admin user"""
    response = client.post('/api/v1/auth/login', json={
        'email': 'admin@example.com',
        'password': 'adminpass123'
    })
    data = response.get_json()
    token = data['access_token']
    return {'Authorization': f'Bearer {token}'} 