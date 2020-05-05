from marshmallow import Schema, fields


class SnmpPollerLogsSchema(Schema):

    id = fields.Integer()
    snmp_poller_id = fields.Integer()
    log_level = fields.String()
    description = fields.String()
    timestamp = fields.DateTime()
