"""
Course Schema

Marshmallow schemas for course validation and serialization.
"""
from marshmallow import Schema, fields, validate, post_load


class CourseCreateSchema(Schema):
    """Schema for creating a new course"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    holes_count = fields.Int(validate=validate.OneOf([6, 9, 18]), missing=18)
    description = fields.Str(allow_none=True)
    club_id = fields.Int(required=True)
    default_tee_set_id = fields.Int(allow_none=True)

    @post_load
    def strip_whitespace(self, data, **kwargs):
        """Strip whitespace from string fields"""
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip() if value else None
        return data


class CourseUpdateSchema(Schema):
    """Schema for updating an existing course"""
    name = fields.Str(validate=validate.Length(min=1, max=120))
    holes_count = fields.Int(validate=validate.OneOf([6, 9, 18]))
    description = fields.Str(allow_none=True)
    club_id = fields.Int()
    default_tee_set_id = fields.Int(allow_none=True)

    @post_load
    def strip_whitespace(self, data, **kwargs):
        """Strip whitespace from string fields"""
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip() if value else None
        return data


class CourseResponseSchema(Schema):
    """Schema for course response"""
    id = fields.Int(dump_only=True)
    name = fields.Str()
    holes_count = fields.Int()
    description = fields.Str(allow_none=True)
    club_id = fields.Int()
    default_tee_set_id = fields.Int(allow_none=True)
    total_par = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CourseWithDetailsSchema(CourseResponseSchema):
    """Schema for course response with holes and tee sets"""
    holes = fields.List(fields.Dict(), dump_only=True)
    tee_sets = fields.List(fields.Dict(), dump_only=True)
    club = fields.Dict(dump_only=True)


class CourseSearchSchema(Schema):
    """Schema for course search parameters"""
    search = fields.Str(validate=validate.Length(min=1))
    club_id = fields.Int()


class DefaultTeeSetSchema(Schema):
    """Schema for setting default tee set"""
    tee_set_id = fields.Int(required=True) 