from marshmallow import Schema, fields, validate
from backend_api.app.common import schema_fields


class OidListSchema(Schema):

    id = schema_fields.Integer()
    brand_name = schema_fields.String(validate=[validate.Length(min=1, max=50, 
        error="Field cannot be blank and must have a character limit of 50.")])
    oid_key = schema_fields.String(validate=[validate.Length(min=1, max=50, 
        error="Field cannot be blank and must have a character limit of 50.")])
    oid = schema_fields.String(validate=[validate.Length(min=1, max=255, 
        error="Field cannot be blank and must have a character limit of 255.")])