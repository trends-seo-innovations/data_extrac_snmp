from flask_restful import Resource
from flask import jsonify
from backend_api.app.api import api
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token
from backend_api.app.models.api_logs import ApiLogs
from backend_api.app import db
from backend_api.app.common.api_utils import ApiUtils
from backend_api.app.common.db_utils import DatabaseUtils
from backend_api.app.models.snmp_poller import SnmpPoller
from backend_api.app.models.snmp_poller_schema import SnmpPollerSchema
from backend_api.app.common.data_view import data_view

class PollerData(Resource):

    api_utils = ApiUtils()
    db_utils = DatabaseUtils()
    poller_schema = SnmpPollerSchema

    def get(self, table_name=None):
        if table_name is None:
            return {'message': 'No table name', 'type': 'TableError'}, 422

        table_name = table_name.replace(' ', '')
        table_not_exists = self.db_utils.check_table_if_not_exist(table_name)

        if not table_not_exists:
            poller_tables = self.db_utils.model_session(SnmpPoller)
            tables = self.db_utils.filter_with_paginate(poller_tables, SnmpPoller, id=None, args=None)
            schema_option = self.api_utils.schema_options(self.poller_schema,'table_name')
            tables_result = SnmpPollerSchema(**schema_option).dump(tables)
            all_poller_tables = [val['table_name'] for val in tables_result]

            if table_name in all_poller_tables:
                args = self.api_utils.optional_parameters()
                result = data_view(args, table_name)
                return jsonify(result)
            else:
                return {'message': 'Invalid table name.', 'type': 'TableError'}, 422
        else:
            return {'message': 'Table does not exist.', 'type': 'TableError'}, 422