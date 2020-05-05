from flask_restful import reqparse
from requests.auth import HTTPBasicAuth
from marshmallow import ValidationError
from backend_api.app.api import db
from backend_api.app import api
from flask import jsonify
from sqlalchemy import exc
import hashlib
import json
import requests
import subprocess
import ipaddress
requests.packages.urllib3.disable_warnings()


class ApiUtils():

    update_commit = db.session

    def __init__(self, *args, **kwargs):
        pass
    
    def parameters(self, Model, *exclude_columns ,**extra_params):
        _model = Model
        parser = reqparse.RequestParser()
        if len(extra_params) != 0:
            for _param, attr in extra_params.items():
                if attr == 'append':
                    parser.add_argument(_param, trim=True, default=[], action=attr)
                else:
                    if _param == 'old_password':
                        parser.add_argument(_param, trim=True, default="", required=True, help="Please fill out this field.")
                    else:
                        parser.add_argument(_param, trim=True, default="")

        for column in _model.__table__.columns:
            if _model.__table__.columns[column.name].primary_key:
                pass
            elif _model.__table__.columns[column.name].nullable:
                parser.add_argument(column.name, type=str)
            else:
                if column.name in exclude_columns:
                    pass
                else:
                    parser.add_argument(column.name, type=str, required=True, help="Please fill out this field.")
                
        return parser.parse_args()

    def parameters_without_model(self, **extra_params):
        parser = reqparse.RequestParser()
        if len(extra_params) != 0:
            for _param, attr in extra_params.items():
                if attr == 'append':
                    parser.add_argument(_param, trim=True, default=[], action=attr)
                elif attr =='int':
                    parser.add_argument(_param, trim=True, type=int)
                else:
                    parser.add_argument(_param, trim=True, default="")
                
        return parser.parse_args()

    def optional_parameters(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start', type=int, default=1,trim=True, location='args', help="invalid value")
        parser.add_argument('limit', type=int, default=0,trim=True, location='args', help="invalid value")
        parser.add_argument('columns', default=None, type=str, location='args',help="invalid value")
        parser.add_argument('include', default='', type=str, location='args',help="invalid value")
        return parser.parse_args()

    def get_paginated_list(self, results, start, limit):
        count = len(results)
        if limit == 0:
            limit = count
        return results[(start - 1):(start - 1 + limit)]


    def schema_options(self,schema,fields):
        if fields is None:
            return {'many': True}
        else:
            list_of_fields = [key for key in schema._declared_fields.keys()]
            _fields = str(fields).replace(' ', '').split(',')
            _fields.append('id')
            new_field = []
            for field in _fields:
                if field in list_of_fields:
                    new_field.append(field)
            return {'only': new_field, 'many': True}

    def validate_data(self, Schema, data):
        try:
            schema = Schema().load(data)
            return schema
        except ValidationError as err:
            raise err.messages
        
    def encrypt_string(self, value):
        sha_signature = hashlib.sha256(value.encode()).hexdigest()
        return sha_signature

    def convert_to_json(self, data):
        _data = json.dumps(data)
        value = json.loads(_data)
        return value

    def get_last_target(self, target):
        data = target.split(".")
        return data[len(data) - 1]

    def check_list_has_empty_string(self, data_list):
        if "" in data_list or '' in data_list:
            return True

    def ip_validator(self, data_list):
        for ip_list in data_list:
            try:
                ipaddress.ip_address(ip_list['ip_address'])
            except:
                return False
        return True
    def oid_validator(self,conn,oid_list):
        oid_raw = conn.select_query('Select oid_key from oid_list')
        oid_main = [oid['oid_key'] for oid in oid_raw]
        result =  all(elem in oid_main  for elem in oid_list)
        return result

        

                
