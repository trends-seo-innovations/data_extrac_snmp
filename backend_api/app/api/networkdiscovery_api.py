from flask import jsonify
from flask import request
from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from backend_api.app.common.api_utils import ApiUtils
from backend_api.app.common.db_utils import DatabaseUtils
from backend_api.app.models.error_schema import ErrorObject
from snmp_util.discovery import network_discovery as NetworkDiscoveryScan
from backend_api.app.models.snmp_poller_schema import NetworkDiscoverySchema
from backend_api.app import logger
from backend_api.app.api import db
import json


class NetworkDiscovery(Resource):

    api_utils = ApiUtils()
    db_utils = DatabaseUtils()

    module_name = 'Network Discovery'

    @jwt_required
    def post(self):
        args = self.api_utils.parameters_without_model(config='append')
        if args["config"]:
            try:
                config = eval(args["config"][0])
                config = NetworkDiscoverySchema().load(config)
                scanner = NetworkDiscoveryScan(config['ip_address'], config['subnet'], config['community_string'])
                result = scanner.run()
                if result:
                    return result 
                else:
                    return {'lists': [], 'type': 'Info', 'message': 'No SNMP Response'}, 200
            except ValidationError as value_error:
                logger.log("Validation encountered on Network Discovery: %s" % (str(value_error)), log_type='ERROR')
                return {'lists': 'Payload error', 'type': 'ValidationError', 'message': 'Validation errors in your request'}, 422
            except Exception as err:
                logger.log("Error encountered on Network Discovery : %s" % str(err), log_type='ERROR')
                return  {'type': 'ValidationError', 'message': 'Invalid Payload'}, 422
        else:
            return {'lists': "No payload", 'type': 'ValidationError', 'message': 'Validation errors in your request'}, 422