"""
TeeSet Schema

Marshmallow schemas for tee set validation and serialization.
"""
from marshmallow import Schema, fields, validate, post_load


class TeeSetCreateSchema(Schema):
    """Schema for creating a new tee set"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    slope_rating = fields.Float(required=True, validate=validate.Range(min=55, max=155))
    course_rating = fields.Float(required=True, validate=validate.Range(min=50, max=90))
    women_slope_rating = fields.Float(validate=validate.Range(min=55, max=155), allow_none=True)
    women_course_rating = fields.Float(validate=validate.Range(min=50, max=90), allow_none=True)
    course_id = fields.Int(required=True)

    @post_load
    def strip_whitespace(self, data, **kwargs):
        """Strip whitespace from string fields"""
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip() if value else None
        return data


class TeeSetUpdateSchema(Schema):
    """Schema for updating an existing tee set"""
    name = fields.Str(validate=validate.Length(min=1, max=50))
    slope_rating = fields.Float(validate=validate.Range(min=55, max=155))
    course_rating = fields.Float(validate=validate.Range(min=50, max=90))
    women_slope_rating = fields.Float(validate=validate.Range(min=55, max=155), allow_none=True)
    women_course_rating = fields.Float(validate=validate.Range(min=50, max=90), allow_none=True)

    @post_load
    def strip_whitespace(self, data, **kwargs):
        """Strip whitespace from string fields"""
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip() if value else None
        return data


class TeeSetResponseSchema(Schema):
    """Schema for tee set response"""
    id = fields.Int(dump_only=True)
    name = fields.Str()
    slope_rating = fields.Float()
    course_rating = fields.Float()
    women_slope_rating = fields.Float(allow_none=True)
    women_course_rating = fields.Float(allow_none=True)
    course_id = fields.Int()
    total_length_meters = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class TeeSetWithPositionsSchema(TeeSetResponseSchema):
    """Schema for tee set response with tee positions"""
    tee_positions = fields.List(fields.Dict(), dump_only=True)


class StandardTeeSetsCreateSchema(Schema):
    """Schema for creating standard tee sets"""
    course_id = fields.Int(required=True)


class GenderRatingQuerySchema(Schema):
    """Schema for gender rating query parameters"""
    gender = fields.Str(validate=validate.OneOf(['M', 'F']), missing='M')


class TeeSetStatisticsSchema(Schema):
    """Schema for tee set statistics response"""
    id = fields.Int()
    name = fields.Str()
    slope_rating = fields.Float()
    course_rating = fields.Float()
    women_slope_rating = fields.Float(allow_none=True)
    women_course_rating = fields.Float(allow_none=True)
    course_id = fields.Int()
    total_length_meters = fields.Int()
    tee_positions = fields.List(fields.Dict(), dump_only=True)
    usage_stats = fields.Dict(dump_only=True)


class TeeSetValidationSchema(Schema):
    """Schema for tee set validation response"""
    valid = fields.Bool()
    errors = fields.List(fields.Str())
    warnings = fields.List(fields.Str())
    tee_set_count = fields.Int() 