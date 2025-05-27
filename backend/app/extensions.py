"""
Flask extensions initialization
"""
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()
migrate = Migrate()
jwt = JWTManager()


@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    # Import here to avoid circular imports
    from app.models.admin_user import AdminUser
    return AdminUser.query.get(int(user_id))


@jwt.user_identity_loader
def user_identity_lookup(user):
    """JWT user identity loader"""
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """JWT user lookup callback"""
    # Import here to avoid circular imports
    from app.models.user import User
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none() 