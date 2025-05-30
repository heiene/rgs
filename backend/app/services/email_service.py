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
                    background-color: #2563eb;
                    border: none;
                    color: white;
                    padding: 15px 32px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    font-weight: 500;
                    margin: 4px 2px;
                    border-radius: 6px;
                    transition: background-color 0.2s ease;
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
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.6;
                    color: #1e293b;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f8fafc;
                }}
                .email-container {{
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
                    border: 1px solid #e2e8f0;
                    overflow: hidden;
                }}
                .header {{
                    background-color: #ffffff;
                    padding: 30px 30px 20px 30px;
                    text-align: center;
                    border-bottom: 1px solid #e2e8f0;
                }}
                .content {{
                    background-color: #ffffff;
                    padding: 30px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding: 20px 30px;
                    background-color: #f8fafc;
                    color: #64748b;
                    font-size: 14px;
                    border-top: 1px solid #e2e8f0;
                }}
                h1 {{
                    color: #1e293b;
                    font-size: 2rem;
                    font-weight: 700;
                    margin: 0;
                    letter-spacing: -0.5px;
                }}
                p {{
                    margin: 0 0 16px 0;
                    color: #374151;
                }}
                ul {{
                    margin: 16px 0;
                    padding-left: 20px;
                }}
                li {{
                    margin-bottom: 8px;
                    color: #374151;
                }}
                strong {{
                    color: #1e293b;
                    font-weight: 600;
                }}
                code {{
                    background-color: #f1f5f9;
                    color: #1e293b;
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h1>{heading}</h1>
                </div>
                <div class="content">
                    {content}
                    {button_html}
                </div>
                <div class="footer">
                    <p>Best regards,<br>
                    The RGS Team</p>
                    <p><small>This is an automated email from RGS (Rykket's Golf Service)</small></p>
                </div>
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
                subject='Welcome to RGS - Rykket\'s Golf Service',
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[user.email]
            )
            
            # Welcome email content
            content = f"""
            <p>Hello {user.first_name},</p>
            
            <p>Welcome to RGS (Rykket's Golf Service) - your personal golf management platform!</p>
            
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