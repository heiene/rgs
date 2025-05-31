"""
Handicap Schema

Marshmallow schemas for handicap validation and serialization.
"""
from marshmallow import Schema, fields, validate
from datetime import date


class HandicapCreateSchema(Schema):
    """Schema for creating a new handicap"""
    user_id = fields.Int(required=True)
    handicap_value = fields.Float(required=True, validate=validate.Range(min=-5, max=54))
    start_date = fields.Date(missing=date.today, format='%Y-%m-%d')
    reason = fields.Str(validate=validate.Length(max=200), allow_none=True, missing='')
    created_by_id = fields.Int(required=True)


class HandicapUpdateSchema(Schema):
    """Schema for updating an existing handicap"""
    handicap_value = fields.Float(validate=validate.Range(min=-5, max=54))
    end_date = fields.Date(allow_none=True)
    reason = fields.Str(validate=validate.Length(max=200))


class HandicapResponseSchema(Schema):
    """Schema for handicap response"""
    id = fields.Int(dump_only=True)
    handicap_value = fields.Float()
    start_date = fields.Date()
    end_date = fields.Date(allow_none=True)
    reason = fields.Str(allow_none=True)
    is_current = fields.Bool(dump_only=True)
    days_active = fields.Int(dump_only=True)
    user_id = fields.Int()
    created_by_id = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True) 