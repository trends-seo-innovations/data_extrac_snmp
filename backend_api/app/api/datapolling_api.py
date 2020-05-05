from flask_restful import Resource
from flask_jwt_extended import jwt_required
from backend_api.app.models.error_schema import ErrorObject
from backend_api.app.common.api_utils import ApiUtils
from backend_api.app.common.db_utils import DatabaseUtils
from snmp_util.reference.device_preview import PollPreview
from backend_api.app.models.poller_data_schema import IpListSchema
from marshmallow import ValidationError
from backend_api.app import logger
import json

class DataPollingApi(Resource):

    api_utils = ApiUtils()
    db_utils = DatabaseUtils()

    module_name = 'Polling Data Preview'


    def post(self):
        args = self.api_utils.parameters_without_model(config='append')

        try:
            config = args['config'][0].replace('\'', '\"')
           
            if len(config) == 0:
                raise ValueError(ErrorObject(type="Config cannot be blank", message="ConfigError").to_json())

            config = json.loads(config)
            config_preview = {
                'ip_list': config['ip_list'],
                'community_string': config['community_string'],
                'oid_list': config['oid_list']
            }

            status = config['ip_list'][0] if config['ip_list'] else ""

            if self.api_utils.check_list_has_empty_string(config_preview['ip_list']) or isinstance(status, str):
                raise ValueError("Invalid IP list value")
            
            for ip in config_preview['ip_list']:
                IpListSchema().load(ip)

            if not isinstance(config_preview['oid_list'], list):
                logger.log("Validation encountered on polling data preview: %s" % ('Invalid oid list values'), log_type='ERROR')
                return {'lists': 'Invalid oid list', 'type': 'ValidationError', 'message': 'Validation errors in your request'}, 422
            poll_preview = PollPreview(config_preview)
            result = poll_preview.run()

            return result
        except ValidationError as value_error:
            logger.log("Validation encountered on polling data preview: %s" % (str(value_error)), log_type='ERROR')
            return {'lists': value_error.messages, 'type': 'ValidationError', 'message': 'Validation errors in your request'}, 422
        except Exception as err:
            logger.log("Error encountered on polling data preview: %s" % str(err), log_type='ERROR')
            return {'type': 'ExceptionType', 'message': str(err)}, 422