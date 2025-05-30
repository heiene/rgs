"""
Round Schema

Simple Marshmallow schemas for round validation and serialization.
"""
from marshmallow import Schema, fields, validate
from datetime import date


class RoundCreateSchema(Schema):
    """Schema for creating a new round"""
    user_id = fields.Int(required=True)
    course_id = fields.Int(required=True)
    tee_set_id = fields.Int(required=True)
    date_played = fields.Date(missing=date.today)
    handicap_used = fields.Float(validate=validate.Range(min=-5, max=54), allow_none=True)


class RoundUpdateSchema(Schema):
    """Schema for updating an existing round"""
    date_played = fields.Date()
    handicap_used = fields.Float(validate=validate.Range(min=-5, max=54), allow_none=True)


class RoundResponseSchema(Schema):
    """Schema for round response"""
    id = fields.Int(dump_only=True)
    date_played = fields.Date()
    handicap_used = fields.Float(allow_none=True)
    course_handicap = fields.Int(allow_none=True)
    course_rating = fields.Float(allow_none=True)
    slope_rating = fields.Float(allow_none=True)
    total_score = fields.Int(allow_none=True)
    total_points = fields.Int(allow_none=True)
    net_score = fields.Int(allow_none=True, dump_only=True)
    differential = fields.Float(allow_none=True)
    is_complete = fields.Bool(dump_only=True)
    user_id = fields.Int()
    course_id = fields.Int()
    tee_set_id = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class RoundWithScoresSchema(RoundResponseSchema):
    """Schema for round response with scores"""
    scores = fields.List(fields.Dict(), dump_only=True) 