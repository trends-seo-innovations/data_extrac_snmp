from marshmallow import Schema, fields, validate
from backend_api.app.common import schema_fields
from marshmallow.validate import Range

class BlacklistSchema(Schema):

    id = schema_fields.Integer()
    snmp_poller_id = schema_fields.Integer(required=True,
        validate=[Range(min=1, error="Invalid value on SNMP poller id")])
    ip_address = schema_fields.String(validate=[validate.Length(min=1, max=50, 
        error="Invalid IP address")])
    brand = schema_fields.String(validate=[validate.Length(min=1, max=50, 
        error="Invalid String")])
    system_description = schema_fields.String(validate=[validate.Length(min=1, max=50, 
        error="Invalid String")])
    system_name = schema_fields.String(validate=[validate.Length(min=1, max=50, 
        error="Invalid String")])