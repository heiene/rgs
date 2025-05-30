"""
Hole Schema

Marshmallow schemas for hole validation and serialization.
"""
from marshmallow import Schema, fields, validate, post_load


class HoleCreateSchema(Schema):
    """Schema for creating a new hole"""
    hole_number = fields.Int(required=True, validate=validate.Range(min=1, max=18))
    par = fields.Int(required=True, validate=validate.Range(min=3, max=6))
    stroke_index = fields.Int(required=True, validate=validate.Range(min=1, max=18))
    course_id = fields.Int(required=True)


class HoleUpdateSchema(Schema):
    """Schema for updating an existing hole"""
    hole_number = fields.Int(validate=validate.Range(min=1, max=18))
    par = fields.Int(validate=validate.Range(min=3, max=6))
    stroke_index = fields.Int(validate=validate.Range(min=1, max=18))


class HoleResponseSchema(Schema):
    """Schema for hole response"""
    id = fields.Int(dump_only=True)
    hole_number = fields.Int()
    par = fields.Int()
    stroke_index = fields.Int()
    course_id = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class HoleWithTeePositionsSchema(HoleResponseSchema):
    """Schema for hole response with tee positions"""
    tee_positions = fields.List(fields.Dict(), dump_only=True)


class StandardHolesCreateSchema(Schema):
    """Schema for creating standard 18 holes"""
    course_id = fields.Int(required=True)
    par_layout = fields.List(fields.Int(validate=validate.Range(min=3, max=6)), 
                            validate=validate.Length(equal=18), 
                            allow_none=True)


class HoleStatisticsSchema(Schema):
    """Schema for hole statistics response"""
    id = fields.Int()
    hole_number = fields.Int()
    par = fields.Int()
    stroke_index = fields.Int()
    course_id = fields.Int()
    tee_positions = fields.List(fields.Dict(), dump_only=True)
    scoring_stats = fields.Dict(allow_none=True, dump_only=True)


class CourseValidationSchema(Schema):
    """Schema for course hole validation response"""
    valid = fields.Bool()
    errors = fields.List(fields.Str())
    warnings = fields.List(fields.Str())
    hole_count = fields.Int()
    expected_holes = fields.Int()
    total_par = fields.Int(allow_none=True) 