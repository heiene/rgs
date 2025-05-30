"""
Authentication API tests
"""
import pytest
from datetime import datetime, timedelta
from app.models.user import User
from app.extensions import db


class TestAuthLogin:
    """Test authentication login endpoint"""
    
    def test_login_success(self, client, test_user):
        """Test successful login with valid credentials"""
        response = client.post('/api/v1/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['user']['email'] == 'test@example.com'
        assert data['user']['first_name'] == 'Test'
        assert data['user']['is_active'] is True
        assert 'is_admin' not in data['user']  # Not included in public user data
    
    def test_login_invalid_email(self, client, test_user):
        """Test login with invalid email"""
        response = client.post('/api/v1/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'testpass123'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
        assert 'Invalid credentials' == data['error']
    
    def test_login_invalid_password(self, client, test_user):
        """Test login with invalid password"""
        response = client.post('/api/v1/auth/login', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
        assert 'Invalid credentials' == data['error']
    
    def test_login_inactive_user(self, client, app):
        """Test login with inactive user"""
        with app.app_context():
            user = User(
                email='inactive@example.com',
                first_name='Inactive',
                last_name='User',
                sex='M',
                is_active=False,
                is_admin=False
            )
            user.set_password('testpass123')
            db.session.add(user)
            db.session.commit()
        
        response = client.post('/api/v1/auth/login', json={
            'email': 'inactive@example.com',
            'password': 'testpass123'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
        assert 'Account is deactivated' == data['error']
    
    def test_login_missing_fields(self, client):
        """Test login with missing required fields"""
        # Missing password
        response = client.post('/api/v1/auth/login', json={
            'email': 'test@example.com'
        })
        assert response.status_code == 400
        
        # Missing email
        response = client.post('/api/v1/auth/login', json={
            'password': 'testpass123'
        })
        assert response.status_code == 400
        
        # Empty payload
        response = client.post('/api/v1/auth/login', json={})
        assert response.status_code == 400


class TestAuthRegister:
    """Test authentication registration endpoint"""
    
    def test_register_success(self, client, app):
        """Test successful user registration"""
        response = client.post('/api/v1/auth/register', json={
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
            'sex': 'F'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'User registered successfully'
        assert data['user']['email'] == 'newuser@example.com'
        assert data['user']['first_name'] == 'New'
        assert data['user']['is_admin'] is False
        
        # Verify user was created in database
        with app.app_context():
            user = User.query.filter_by(email='newuser@example.com').first()
            assert user is not None
            assert user.check_password('newpass123')
    
    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email"""
        response = client.post('/api/v1/auth/register', json={
            'email': 'test@example.com',  # Already exists
            'password': 'newpass123',
            'first_name': 'Another',
            'last_name': 'User',
            'sex': 'M'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'Email already registered' in data['message']
    
    def test_register_invalid_email_format(self, client):
        """Test registration with invalid email format"""
        response = client.post('/api/v1/auth/register', json={
            'email': 'invalid-email',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
            'sex': 'M'
        })
        
        assert response.status_code == 400
    
    def test_register_weak_password(self, client):
        """Test registration with weak password"""
        response = client.post('/api/v1/auth/register', json={
            'email': 'newuser@example.com',
            'password': '123',  # Too short
            'first_name': 'New',
            'last_name': 'User',
            'sex': 'M'
        })
        
        assert response.status_code == 400
    
    def test_register_missing_fields(self, client):
        """Test registration with missing required fields"""
        incomplete_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
            # Missing first_name, last_name, sex
        }
        
        response = client.post('/api/v1/auth/register', json=incomplete_data)
        assert response.status_code == 400


class TestPasswordReset:
    """Test password reset functionality"""
    
    def test_forgot_password_success(self, client, test_user):
        """Test successful password reset request"""
        response = client.post('/api/v1/auth/forgot-password', json={
            'email': 'test@example.com'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'Password reset email sent' in data['message']
    
    def test_forgot_password_nonexistent_email(self, client):
        """Test password reset request for nonexistent email"""
        response = client.post('/api/v1/auth/forgot-password', json={
            'email': 'nonexistent@example.com'
        })
        
        # Should return success to prevent email enumeration
        assert response.status_code == 200
        data = response.get_json()
        assert 'Password reset email sent' in data['message']
    
    def test_reset_password_success(self, client, app, test_user):
        """Test successful password reset with valid token"""
        # First request password reset to get token
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            from app.services.email_service import EmailService
            email_service = EmailService()
            token = email_service._generate_reset_token(user)
            
            # Reset password with token
            response = client.post('/api/v1/auth/reset-password', json={
                'token': token,
                'new_password': 'newpassword123'
            })
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'Password reset successfully' in data['message']
            
            # Verify new password works
            user = User.query.filter_by(email='test@example.com').first()
            assert user.check_password('newpassword123')
    
    def test_reset_password_invalid_token(self, client):
        """Test password reset with invalid token"""
        response = client.post('/api/v1/auth/reset-password', json={
            'token': 'invalid-token',
            'new_password': 'newpassword123'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'Invalid or expired token' in data['message']
    
    def test_reset_password_expired_token(self, client, app, test_user):
        """Test password reset with expired token"""
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            # Set expired reset token
            user.password_reset_expires = datetime.utcnow() - timedelta(hours=2)
            user.password_reset_token = 'expired-token'
            db.session.commit()
            
            response = client.post('/api/v1/auth/reset-password', json={
                'token': 'expired-token',
                'new_password': 'newpassword123'
            })
            
            assert response.status_code == 400
            data = response.get_json()
            assert 'Invalid or expired token' in data['message']


class TestTokenValidation:
    """Test JWT token validation"""
    
    def test_valid_token_access(self, client, auth_headers):
        """Test accessing protected endpoint with valid token"""
        response = client.get('/api/v1/auth/me', headers=auth_headers)
        assert response.status_code == 200
    
    def test_missing_token_access(self, client):
        """Test accessing protected endpoint without token"""
        response = client.get('/api/v1/auth/me')
        assert response.status_code == 401
    
    def test_invalid_token_access(self, client):
        """Test accessing protected endpoint with invalid token"""
        headers = {'Authorization': 'Bearer invalid-token'}
        response = client.get('/api/v1/auth/me', headers=headers)
        assert response.status_code == 422  # Malformed token returns 422
    
    def test_malformed_authorization_header(self, client):
        """Test with malformed authorization header"""
        headers = {'Authorization': 'InvalidFormat token'}
        response = client.get('/api/v1/auth/me', headers=headers)
        assert response.status_code == 401 