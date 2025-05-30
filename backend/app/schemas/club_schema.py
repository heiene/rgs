"""
Club Schema

Marshmallow schemas for club validation and serialization.
"""
from marshmallow import Schema, fields, validate, post_load
from app.services.timezone_service import TimezoneService


class ClubCreateSchema(Schema):
    """Schema for creating a new club"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    description = fields.Str(allow_none=True)
    website = fields.Url(allow_none=True)
    email = fields.Email(allow_none=True)
    phone = fields.Str(validate=validate.Length(max=20), allow_none=True)
    address = fields.Str(validate=validate.Length(max=200), allow_none=True)
    city = fields.Str(validate=validate.Length(max=100), allow_none=True)
    country = fields.Str(validate=validate.Length(max=100), allow_none=True)
    postal_code = fields.Str(validate=validate.Length(max=20), allow_none=True)
    timezone = fields.Str(validate=validate.OneOf(TimezoneService.common_golf_timezones()), 
                          missing='Europe/Oslo')

    @post_load
    def strip_whitespace(self, data, **kwargs):
        """Strip whitespace from string fields"""
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip() if value else None
        return data


class ClubUpdateSchema(Schema):
    """Schema for updating an existing club"""
    name = fields.Str(validate=validate.Length(min=1, max=120))
    description = fields.Str(allow_none=True)
    website = fields.Url(allow_none=True)
    email = fields.Email(allow_none=True)
    phone = fields.Str(validate=validate.Length(max=20), allow_none=True)
    address = fields.Str(validate=validate.Length(max=200), allow_none=True)
    city = fields.Str(validate=validate.Length(max=100), allow_none=True)
    country = fields.Str(validate=validate.Length(max=100), allow_none=True)
    postal_code = fields.Str(validate=validate.Length(max=20), allow_none=True)
    timezone = fields.Str(validate=validate.OneOf(TimezoneService.common_golf_timezones()))

    @post_load
    def strip_whitespace(self, data, **kwargs):
        """Strip whitespace from string fields"""
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip() if value else None
        return data


class ClubResponseSchema(Schema):
    """Schema for club response"""
    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str(allow_none=True)
    website = fields.Str(allow_none=True)
    email = fields.Str(allow_none=True)
    phone = fields.Str(allow_none=True)
    address = fields.Str(allow_none=True)
    city = fields.Str(allow_none=True)
    country = fields.Str(allow_none=True)
    postal_code = fields.Str(allow_none=True)
    timezone = fields.Str()
    full_address = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ClubWithCoursesSchema(ClubResponseSchema):
    """Schema for club response with courses"""
    courses = fields.List(fields.Dict(), dump_only=True)
    course_count = fields.Int(dump_only=True)


class ClubSearchSchema(Schema):
    """Schema for club search parameters"""
    query = fields.Str(required=True, validate=validate.Length(min=1))
    country = fields.Str(validate=validate.Length(max=100), allow_none=True) 