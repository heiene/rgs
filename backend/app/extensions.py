"""
Flask extensions initialization
"""
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()


@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    # TODO: Uncomment when models are created
    # from app.models.admin_user import AdminUser
    # return AdminUser.query.get(int(user_id))
    return None


@jwt.user_identity_loader
def user_identity_lookup(user):
    """JWT user identity loader"""
    # Handle both User objects and integer IDs
    if hasattr(user, 'id'):
        return user.id
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """JWT user lookup callback"""
    from app.models.user import User
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none() 