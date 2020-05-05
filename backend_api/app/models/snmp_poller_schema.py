from marshmallow import Schema, fields, validate
from backend_api.app.common import schema_fields
from marshmallow.validate import Range


class SnmpPollerSchema(Schema):
    id = schema_fields.Integer()
    name = schema_fields.String(validate=[validate.Length(min=1, max=50, 
        error="Field cannot be blank and must have a character limit of 50.")])
    ip_address = schema_fields.String(validate=[
        validate.Length(min=1, max=50, error="Field cannot be blank and must have a character limit of 50."),
        validate.Regexp('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',error="Invalid IP address")])
    subnet = schema_fields.Integer(validate=[Range(min=1, max=32,
        error="Invalid subnet value")])
    community_string = schema_fields.String(validate=[validate.Length(min=1, max=255, 
        error="Field cannot be blank and must have a character limit of 255.")])
    interval = schema_fields.Integer(validate=[Range(min=30, max=86400,
        error="interval must have a minimum value of 30 seconds and maximum value of 86400")])
    table_name = schema_fields.String(validate=[
        validate.Length(min=1,max=50, error="Field cannot be blank and must have a character limit of 50."), 
        validate.Regexp('^[a-zA-Z][a-zA-Z0-9._]{0,50}$', error="Field should not start with special or numeric character and ending with special character and must not have spaces.")])
    status = schema_fields.Integer(allow_none=True, default=0)
    pid = schema_fields.Integer(allow_none=True, default=0)


class NetworkDiscoverySchema(Schema):
    ip_address = schema_fields.String(validate=[validate.Length(min=1, max=50, 
        error="Field cannot be blank and must have a character limit of 50."),
        validate.Regexp('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',error="Invalid IP address")])
    subnet = schema_fields.Integer(validate=[Range(min=1, max=32,
        error="Invalid subnet value")])
    community_string = schema_fields.String(validate=[validate.Length(min=1, max=255, 
        error="Field cannot be blank and must have a character limit of 255.")])