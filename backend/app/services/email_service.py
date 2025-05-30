"""
Email Service

Contains all business logic for email operations.
Handles password reset emails, welcome emails, etc.
"""
import os
import secrets
from datetime import datetime, timedelta
from typing import Optional
from flask import current_app, render_template_string
from flask_mail import Message
from app.extensions import mail, db
from app.models.user import User


class EmailService:
    """Service class for email operations"""

    @staticmethod
    def send_password_reset_email(email: str) -> bool:
        """Send password reset email to user"""
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Don't reveal if email exists or not for security
            return True
        
        # Generate reset token
        token = secrets.token_urlsafe(32)
        user.password_reset_token = token
        user.password_reset_expires = datetime.utcnow() + timedelta(hours=1)  # 1 hour expiry
        
        db.session.commit()
        
        # Send email
        try:
            msg = Message(
                subject='RGS - Password Reset Request',
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[email]
            )
            
            # Email template
            email_body = f"""
            <h2>Password Reset Request</h2>
            <p>Hello {user.first_name},</p>
            
            <p>You have requested a password reset for your RGS account.</p>
            
            <p>Your reset token is: <strong>{token}</strong></p>
            
            <p>This token will expire in 1 hour.</p>
            
            <p>To reset your password, use this token with the password reset endpoint:</p>
            <p><code>POST /api/v1/auth/reset-password</code></p>
            
            <p>If you did not request this reset, please ignore this email.</p>
            
            <br>
            <p>Best regards,<br>
            The RGS Team</p>
            """
            
            msg.html = email_body
            mail.send(msg)
            return True
            
        except Exception as e:
            current_app.logger.error(f"Failed to send password reset email: {str(e)}")
            return False

    @staticmethod
    def send_welcome_email(user: User) -> bool:
        """Send welcome email to new user"""
        try:
            msg = Message(
                subject='Welcome to RGS - Your Golf Management System',
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[user.email]
            )
            
            # Welcome email template
            email_body = f"""
            <h2>Welcome to RGS!</h2>
            <p>Hello {user.first_name},</p>
            
            <p>Welcome to RGS (Round Golf System) - your personal golf management platform!</p>
            
            <p>Your account has been successfully created with the following details:</p>
            <ul>
                <li><strong>Email:</strong> {user.email}</li>
                <li><strong>Name:</strong> {user.full_name}</li>
                <li><strong>Preferred Distance Unit:</strong> {user.distance_unit}</li>
                <li><strong>Timezone:</strong> {user.timezone}</li>
            </ul>
            
            <p>You can now start:</p>
            <ul>
                <li>Adding your favorite golf courses</li>
                <li>Recording your rounds and scores</li>
                <li>Tracking your handicap progress</li>
                <li>Analyzing your golf statistics</li>
            </ul>
            
            <p>If you have any questions, feel free to reach out to our support team.</p>
            
            <br>
            <p>Best regards,<br>
            The RGS Team</p>
            """
            
            msg.html = email_body
            mail.send(msg)
            return True
            
        except Exception as e:
            current_app.logger.error(f"Failed to send welcome email: {str(e)}")
            return False

    @staticmethod
    def verify_reset_token(token: str) -> Optional[User]:
        """Verify password reset token and return user if valid"""
        user = User.query.filter_by(password_reset_token=token).first()
        
        if not user:
            return None
        
        # Check if token has expired
        if user.password_reset_expires and user.password_reset_expires < datetime.utcnow():
            # Clear expired token
            user.password_reset_token = None
            user.password_reset_expires = None
            db.session.commit()
            return None
        
        return user

    @staticmethod
    def clear_reset_token(user: User) -> None:
        """Clear password reset token after successful reset"""
        user.password_reset_token = None
        user.password_reset_expires = None
        db.session.commit()

    @staticmethod
    def send_password_changed_notification(user: User) -> bool:
        """Send notification email when password is changed"""
        try:
            msg = Message(
                subject='RGS - Password Changed Successfully',
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[user.email]
            )
            
            email_body = f"""
            <h2>Password Changed</h2>
            <p>Hello {user.first_name},</p>
            
            <p>Your RGS account password has been successfully changed.</p>
            
            <p>If you did not make this change, please contact our support team immediately.</p>
            
            <p>Change time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
            
            <br>
            <p>Best regards,<br>
            The RGS Team</p>
            """
            
            msg.html = email_body
            mail.send(msg)
            return True
            
        except Exception as e:
            current_app.logger.error(f"Failed to send password change notification: {str(e)}")
            return False 