from marshmallow import Schema, fields, validate


class String(fields.String):
    default_error_messages = {
        "null": "Field must not be empty",
        "invalid": "Not a valid string.",
        "invalid_utf8": "Not a valid utf-8 string.",
        "required": "Please fill out this field"
    }

class Integer(fields.Integer):
    default_error_messages = {
        "null": "Field must not be empty",
        "invalid": "Field must be a counting number",
        "required": "Please fill out this field"
    }
class Number(fields.Number):
    default_error_messages = {
        "invalid": "Not a valid number.",
        "too_large": "Number too large.",
    }
class Boolean(fields.Boolean):
     default_error_messages = {"invalid": "Not a valid boolean."}

class List(fields.List):
    default_error_messages = {
        "required": "Please fill out this field"
    }