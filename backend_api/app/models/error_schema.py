from marshmallow import Schema, fields, pre_load
from backend_api.app.common import schema_fields
import json

class ErrorObject(object):

    def __init__(self, message=None, type=None):
        self.message = message
        self.type = type
    
    def to_json(self):
        return self.__dict__


    # type = schema_fields.String()
    # message = schema_fields.String()

    

    # type = schema_fields.String()
    # message = schema_fields.String()

