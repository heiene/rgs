"""
User Schema

Marshmallow schemas for user validation and serialization.
"""
from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class UserCreateSchema(Schema):
    """Schema for creating a new user"""
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    sex = fields.Str(validate=validate.OneOf(['M', 'F']), missing='M')
    distance_unit = fields.Str(validate=validate.OneOf(['meters', 'yards']), missing='meters')
    timezone = fields.Str(missing='Europe/Oslo')
    country = fields.Str(validate=validate.Length(max=100))
    city = fields.Str(validate=validate.Length(max=100))
    address = fields.Str(validate=validate.Length(max=200))
    postal_code = fields.Str(validate=validate.Length(max=20))
    home_club_id = fields.Int(allow_none=True)
    preferred_theme_id = fields.Int(allow_none=True)
    is_admin = fields.Bool(missing=False)


class UserUpdateSchema(Schema):
    """Schema for updating an existing user"""
    first_name = fields.Str(validate=validate.Length(min=1, max=50))
    last_name = fields.Str(validate=validate.Length(min=1, max=50))
    sex = fields.Str(validate=validate.OneOf(['M', 'F']))
    distance_unit = fields.Str(validate=validate.OneOf(['meters', 'yards']))
    timezone = fields.Str()
    country = fields.Str(validate=validate.Length(max=100))
    city = fields.Str(validate=validate.Length(max=100))
    address = fields.Str(validate=validate.Length(max=200))
    postal_code = fields.Str(validate=validate.Length(max=20))
    home_club_id = fields.Int(allow_none=True)
    preferred_theme_id = fields.Int(allow_none=True)
    is_active = fields.Bool()


class UserPasswordUpdateSchema(Schema):
    """Schema for updating user password"""
    current_password = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=validate.Length(min=8))
    confirm_password = fields.Str(required=True)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data.get('new_password') != data.get('confirm_password'):
            raise ValidationError('New passwords do not match', field_names=['confirm_password'])


class UserResponseSchema(Schema):
    """Schema for user response (basic info)"""
    id = fields.Int(dump_only=True)
    email = fields.Email()
    first_name = fields.Str()
    last_name = fields.Str()
    full_name = fields.Str(dump_only=True)
    sex = fields.Str()
    is_active = fields.Bool()
    distance_unit = fields.Str()
    timezone = fields.Str()
    country = fields.Str(allow_none=True)
    city = fields.Str(allow_none=True)
    address = fields.Str(allow_none=True)
    postal_code = fields.Str(allow_none=True)
    full_address = fields.Str(dump_only=True, allow_none=True)
    home_club_id = fields.Int(allow_none=True)
    preferred_theme_id = fields.Int(allow_none=True)
    current_handicap = fields.Float(dump_only=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    last_login = fields.DateTime(dump_only=True, allow_none=True)


class UserAdminResponseSchema(UserResponseSchema):
    """Schema for user response with admin fields"""
    is_admin = fields.Bool()
    password_reset_token = fields.Str(allow_none=True)
    password_reset_expires = fields.DateTime(allow_none=True)


class UserListSchema(Schema):
    """Schema for user list response"""
    users = fields.List(fields.Nested(UserResponseSchema))
    total = fields.Int()
    page = fields.Int()
    per_page = fields.Int()
    pages = fields.Int()


class UserSearchSchema(Schema):
    """Schema for user search parameters"""
    search = fields.Str()
    club_id = fields.Int()
    is_active = fields.Bool()
    page = fields.Int(missing=1, validate=validate.Range(min=1))
    per_page = fields.Int(missing=20, validate=validate.Range(min=1, max=100)) 