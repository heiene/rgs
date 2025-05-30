"""
Score Schema

Simple Marshmallow schemas for score validation and serialization.
"""
from marshmallow import Schema, fields, validate


class ScoreCreateSchema(Schema):
    """Schema for creating a new score"""
    round_id = fields.Int(required=True)
    hole_id = fields.Int(required=True)
    strokes = fields.Int(required=True, validate=validate.Range(min=1, max=20))


class ScoreUpdateSchema(Schema):
    """Schema for updating an existing score"""
    strokes = fields.Int(validate=validate.Range(min=1, max=20))


class ScoreResponseSchema(Schema):
    """Schema for score response"""
    id = fields.Int(dump_only=True)
    strokes = fields.Int()
    points = fields.Int(allow_none=True)
    score_to_par = fields.Str(dump_only=True, allow_none=True)
    score_name = fields.Str(dump_only=True, allow_none=True)
    round_id = fields.Int()
    hole_id = fields.Int()
    hole_number = fields.Int(dump_only=True, allow_none=True)
    hole_par = fields.Int(dump_only=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class BulkScoreCreateSchema(Schema):
    """Schema for creating multiple scores"""
    round_id = fields.Int(required=True)
    hole_scores = fields.List(fields.Dict(), required=True, validate=validate.Length(min=1))


class HoleScoreSchema(Schema):
    """Schema for individual hole score in bulk operations"""
    hole_number = fields.Int(required=True, validate=validate.Range(min=1, max=18))
    strokes = fields.Int(required=True, validate=validate.Range(min=1, max=20)) 