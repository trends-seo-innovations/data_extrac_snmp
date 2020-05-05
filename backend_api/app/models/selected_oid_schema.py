from marshmallow import Schema, fields, validate
from backend_api.app.common import schema_fields
from marshmallow.validate import Range

class SelectedOidSchema(Schema):

    id = schema_fields.Integer()
    snmp_poller_id = schema_fields.Integer(required=True,
        validate=[Range(min=1, error="Invalid value on SNMP poller id")])
    oid_key = schema_fields.String(validate=[validate.Length(min=1, max=50, 
        error="Field cannot be blank and must have a character limit of 50.")])