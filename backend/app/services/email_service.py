"""
Email Service

Contains all business logic for email operations.
Handles password reset emails, welcome emails, etc.
"""
import os
import secrets
from datetime import datetime, timedelta
from typing import Optional, Union
from flask import current_app, render_template_string
from flask_mail import Message
from app.extensions import mail, db
from app.models.user import User


class EmailService:
    """Service class for email operations"""

    @staticmethod
    def send_password_reset_email(email_or_user: Union[str, User]) -> bool:
        """Send password reset email to user"""
        # Handle both string email and User object
        if isinstance(email_or_user, User):
            user = email_or_user
            email = user.email
        else:
            email = email_or_user
            user = User.query.filter_by(email=email).first()
        
        if not user:
            # Don't reveal if email exists or not for security
            return True
        
        # Generate reset token
        token = EmailService._generate_reset_token(user)
        
        # Send email
        try:
            msg = Message(
                subject='RGS - Password Reset Request',
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[email]
            )
            
            # Get reset URL
            reset_url = EmailService._get_reset_url(token)
            
            # Email template using the HTML template method
            email_body = EmailService._create_html_email(
                title='RGS - Password Reset Request',
                heading='Password Reset Request',
                content=f"""
                <p>Hello {user.first_name},</p>
                
                <p>You have requested a password reset for your RGS account.</p>
                
                <p>Your reset token is: <strong>{token}</strong></p>
                
                <p>This token will expire in 1 hour.</p>
                
                <p>To reset your password, use this token with the password reset endpoint:</p>
                <p><code>POST /api/v1/auth/reset-password</code></p>
                
                <p>If you did not request this reset, please ignore this email.</p>
                """,
                button_text='Reset Password',
                button_url=reset_url
            )
            
            msg.html = email_body
            mail.send(msg)
            return True
            
        except Exception as e:
            current_app.logger.error(f"Failed to send password reset email: {str(e)}")
            return False

    @staticmethod
    def _generate_reset_token(user: User) -> str:
        """Generate and store password reset token for user"""
        token = secrets.token_urlsafe(32)
        
        # Make sure we're working with an attached object
        if not user in db.session:
            # Re-query to get attached object
            user = User.query.filter_by(id=user.id).first()
            if not user:
                raise ValueError("User not found")
        
        user.password_reset_token = token
        user.password_reset_expires = datetime.utcnow() + timedelta(hours=1)  # 1 hour expiry
        
        db.session.commit()
        
        # Refresh the user object to ensure it reflects the database state
        db.session.refresh(user)
        
        return token

    @staticmethod
    def _get_reset_url(token: str) -> str:
        """Generate password reset URL with token"""
        base_url = current_app.config.get('FRONTEND_URL', 'http://localhost:3000')
        return f"{base_url}/reset-password?token={token}"

    @staticmethod
    def _create_html_email(title: str, heading: str, content: str, 
                          button_text: Optional[str] = None, 
                          button_url: Optional[str] = None) -> str:
        """Create HTML email template with consistent styling"""
        
        button_html = ""
        if button_text and button_url:
            button_html = f"""
            <div style="text-align: center; margin: 30px 0;">
                <a href="{button_url}" style="
                    background-color: #4CAF50;
                    border: none;
                    color: white;
                    padding: 15px 32px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    border-radius: 4px;
                ">{button_text}</a>
            </div>
            """
        
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    text-align: center;
                    border-radius: 8px 8px 0 0;
                }}
                .content {{
                    background-color: #ffffff;
                    padding: 30px;
                    border-radius: 0 0 8px 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 14px;
                }}
                code {{
                    background-color: #f1f1f1;
                    padding: 2px 4px;
                    border-radius: 3px;
                    font-family: monospace;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1 style="color: #4CAF50; margin: 0;">{heading}</h1>
            </div>
            <div class="content">
                {content}
                {button_html}
            </div>
            <div class="footer">
                <p>Best regards,<br>
                The RGS Team</p>
                <p><small>This is an automated email from RGS (Round Golf System)</small></p>
            </div>
        </body>
        </html>
        """
        
        return html_template

    @staticmethod
    def send_welcome_email(user: User) -> bool:
        """Send welcome email to new user"""
        try:
            msg = Message(
                subject='Welcome to RGS - Your Golf Management System',
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[user.email]
            )
            
            # Welcome email content
            content = f"""
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
            """
            
            # Use the HTML template
            email_body = EmailService._create_html_email(
                title='Welcome to RGS',
                heading='Welcome to RGS!',
                content=content,
                button_text='Get Started',
                button_url=current_app.config.get('FRONTEND_URL', 'http://localhost:3000')
            )
            
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
        # Make sure we're working with an attached object
        if not user in db.session:
            # Re-query to get attached object
            user = User.query.filter_by(id=user.id).first()
            if not user:
                raise ValueError("User not found")
        
        user.password_reset_token = None
        user.password_reset_expires = None
        db.session.commit()
        
        # Refresh the user object to ensure it reflects the database state
        db.session.refresh(user)

    @staticmethod
    def send_password_changed_notification(user: User) -> bool:
        """Send notification email when password is changed"""
        try:
            msg = Message(
                subject='RGS - Password Changed Successfully',
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[user.email]
            )
            
            # Password changed content
            content = f"""
            <p>Hello {user.first_name},</p>
            
            <p>Your RGS account password has been successfully changed.</p>
            
            <p>If you did not make this change, please contact our support team immediately.</p>
            
            <p>Change time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
            """
            
            # Use the HTML template
            email_body = EmailService._create_html_email(
                title='RGS - Password Changed',
                heading='Password Changed Successfully',
                content=content
            )
            
            msg.html = email_body
            mail.send(msg)
            return True
            
        except Exception as e:
            current_app.logger.error(f"Failed to send password change notification: {str(e)}")
            return False 