"""
Email Service tests
"""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from app.services.email_service import EmailService
from app.models.user import User
from app.extensions import db


class TestEmailService:
    """Test EmailService functionality"""
    
    def test_email_service_initialization(self, app):
        """Test EmailService can be initialized"""
        with app.app_context():
            service = EmailService()
            assert service is not None
    
    @patch('app.services.email_service.mail.send')
    def test_send_password_reset_email(self, mock_send, app, test_user):
        """Test sending password reset email"""
        with app.app_context():
            service = EmailService()
            
            result = service.send_password_reset_email(test_user)
            
            assert result is True
            assert mock_send.called
            
            # Verify user has reset token and expiry set
            user = User.query.filter_by(email='test@example.com').first()
            assert user.password_reset_token is not None
            assert user.password_reset_expires is not None
            assert user.password_reset_expires > datetime.utcnow()
    
    @patch('app.services.email_service.mail.send')
    def test_send_welcome_email(self, mock_send, app, test_user):
        """Test sending welcome email"""
        with app.app_context():
            service = EmailService()
            
            result = service.send_welcome_email(test_user)
            
            assert result is True
            assert mock_send.called
    
    @patch('app.services.email_service.mail.send')
    def test_send_password_changed_notification(self, mock_send, app, test_user):
        """Test sending password changed notification"""
        with app.app_context():
            service = EmailService()
            
            result = service.send_password_changed_notification(test_user)
            
            assert result is True
            assert mock_send.called
    
    def test_generate_reset_token(self, app, test_user):
        """Test reset token generation"""
        with app.app_context():
            service = EmailService()
            
            token = service._generate_reset_token(test_user)
            
            assert token is not None
            assert len(token) > 10  # Should be a reasonable length
            
            # Verify user has token and expiry set
            user = User.query.filter_by(email='test@example.com').first()
            assert user.password_reset_token == token
            assert user.password_reset_expires is not None
    
    def test_verify_reset_token_valid(self, app, test_user):
        """Test verifying valid reset token"""
        with app.app_context():
            service = EmailService()
            
            # Generate token
            token = service._generate_reset_token(test_user)
            
            # Verify token
            user = service.verify_reset_token(token)
            
            assert user is not None
            assert user.email == test_user.email
    
    def test_verify_reset_token_invalid(self, app):
        """Test verifying invalid reset token"""
        with app.app_context():
            service = EmailService()
            
            user = service.verify_reset_token('invalid-token')
            
            assert user is None
    
    def test_verify_reset_token_expired(self, app, test_user):
        """Test verifying expired reset token"""
        with app.app_context():
            service = EmailService()
            
            # Set expired token manually
            expired_time = datetime.utcnow() - timedelta(hours=2)
            test_user.password_reset_token = 'expired-token'
            test_user.password_reset_expires = expired_time
            db.session.commit()
            
            user = service.verify_reset_token('expired-token')
            
            assert user is None
    
    def test_clear_reset_token(self, app, test_user):
        """Test clearing reset token"""
        with app.app_context():
            service = EmailService()
            
            # Set token first
            service._generate_reset_token(test_user)
            
            # Verify token is set
            user = User.query.filter_by(email='test@example.com').first()
            assert user.password_reset_token is not None
            
            # Clear token
            service.clear_reset_token(test_user)
            
            # Verify token is cleared
            user = User.query.filter_by(email='test@example.com').first()
            assert user.password_reset_token is None
            assert user.password_reset_expires is None
    
    @patch('app.services.email_service.mail.send')
    def test_email_sending_failure(self, mock_send, app, test_user):
        """Test handling email sending failures"""
        with app.app_context():
            # Mock mail.send to raise an exception
            mock_send.side_effect = Exception("SMTP Error")
            
            service = EmailService()
            
            result = service.send_welcome_email(test_user)
            
            assert result is False
    
    def test_html_email_content(self, app, test_user):
        """Test that emails contain proper HTML content"""
        with app.app_context():
            service = EmailService()
            
            # Test that _create_html_email generates proper HTML
            html_content = service._create_html_email(
                title="Test Email",
                heading="Test Heading",
                content="Test content with <strong>formatting</strong>",
                button_text="Test Button",
                button_url="https://example.com"
            )
            
            assert '<html>' in html_content
            assert 'Test Email' in html_content
            assert 'Test Heading' in html_content
            assert 'Test content with <strong>formatting</strong>' in html_content
            assert 'Test Button' in html_content
            assert 'https://example.com' in html_content
    
    def test_reset_url_generation(self, app, test_user):
        """Test password reset URL generation"""
        with app.app_context():
            service = EmailService()
            
            token = service._generate_reset_token(test_user)
            reset_url = service._get_reset_url(token)
            
            assert reset_url is not None
            assert token in reset_url
            assert 'reset-password' in reset_url


class TestEmailServiceIntegration:
    """Integration tests for EmailService with Flask-Mail"""
    
    def test_mail_configuration(self, app):
        """Test that mail is properly configured"""
        with app.app_context():
            from app.extensions import mail
            
            assert mail is not None
            assert app.config.get('MAIL_SERVER') is not None
            assert app.config.get('MAIL_PORT') is not None
    
    @patch('app.services.email_service.mail.send')
    def test_email_context_rendering(self, mock_send, app, test_user):
        """Test that email templates render with proper context"""
        with app.app_context():
            service = EmailService()
            
            service.send_password_reset_email(test_user)
            
            # Get the message that would have been sent
            assert mock_send.called
            call_args = mock_send.call_args[0][0]  # First argument (Message object)
            
            assert test_user.first_name in call_args.html
            assert 'password reset' in call_args.html.lower()
            assert call_args.recipients == [test_user.email] 