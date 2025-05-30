"""
TeePosition Schema

Marshmallow schemas for tee position validation and serialization.
"""
from marshmallow import Schema, fields, validate, post_load


class TeePositionCreateSchema(Schema):
    """Schema for creating a new tee position"""
    hole_id = fields.Int(required=True)
    tee_set_id = fields.Int(required=True)
    length = fields.Int(required=True, validate=validate.Range(min=50, max=700))


class TeePositionUpdateSchema(Schema):
    """Schema for updating an existing tee position"""
    length = fields.Int(validate=validate.Range(min=50, max=700))


class TeePositionResponseSchema(Schema):
    """Schema for tee position response"""
    id = fields.Int(dump_only=True)
    length = fields.Int()
    length_unit = fields.Str(dump_only=True)
    length_meters = fields.Int(dump_only=True)
    length_yards = fields.Float(dump_only=True)
    hole_id = fields.Int()
    tee_set_id = fields.Int()
    hole_number = fields.Int(dump_only=True)
    par = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class TeePositionBulkCreateSchema(Schema):
    """Schema for bulk creating tee positions"""
    tee_set_id = fields.Int(required=True)
    distances = fields.List(fields.Int(validate=validate.Range(min=50, max=700)), 
                           required=True, validate=validate.Length(min=1))


class StandardDistancesCreateSchema(Schema):
    """Schema for creating standard distances by par"""
    tee_set_id = fields.Int(required=True)
    difficulty_level = fields.Str(validate=validate.OneOf(['easy', 'medium', 'hard', 'championship']), 
                                 missing='medium')


class TeePositionBulkUpdateSchema(Schema):
    """Schema for bulk updating tee position distances"""
    tee_set_id = fields.Int(required=True)
    distances = fields.List(fields.Dict(), required=True, validate=validate.Length(min=1))


class DistanceUpdateSchema(Schema):
    """Schema for individual distance update"""
    hole_number = fields.Int(required=True, validate=validate.Range(min=1, max=18))
    length = fields.Int(required=True, validate=validate.Range(min=50, max=700))


class TeePositionStatisticsSchema(Schema):
    """Schema for tee position statistics response"""
    tee_set_id = fields.Int()
    tee_set_name = fields.Str()
    total_positions = fields.Int()
    total_length_meters = fields.Int()
    total_length_yards = fields.Int()
    average_distance = fields.Int()
    shortest_hole = fields.Dict(allow_none=True)
    longest_hole = fields.Dict(allow_none=True)
    distance_breakdown = fields.Dict()


class UnitQuerySchema(Schema):
    """Schema for unit query parameter"""
    unit = fields.Str(validate=validate.OneOf(['meters', 'yards']), missing='meters') 