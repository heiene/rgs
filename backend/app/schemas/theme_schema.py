"""
Theme Schema

Marshmallow schemas for theme validation and serialization.
"""
from marshmallow import Schema, fields, validate, post_load


class ThemeCreateSchema(Schema):
    """Schema for creating a new theme"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    description = fields.Str(allow_none=True)

    @post_load
    def strip_whitespace(self, data, **kwargs):
        """Strip whitespace from string fields"""
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip() if value else None
        return data


class ThemeUpdateSchema(Schema):
    """Schema for updating an existing theme"""
    name = fields.Str(validate=validate.Length(min=1, max=50))
    description = fields.Str(allow_none=True)

    @post_load
    def strip_whitespace(self, data, **kwargs):
        """Strip whitespace from string fields"""
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip() if value else None
        return data


class ThemeResponseSchema(Schema):
    """Schema for theme response"""
    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True) 