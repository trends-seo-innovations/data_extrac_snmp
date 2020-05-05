from flask_restful import Resource
from backend_api.app.common.api_utils import ApiUtils
from backend_api.app.common.db_utils import DatabaseUtils
from backend_api.app.api import db
from flask_jwt_extended import jwt_required
from flask import jsonify


class SchemaAPI(Resource):
    
    db_utils = DatabaseUtils()


    def get(self, table_name=None):
        if table_name is None:
            default = self.db_utils.get_all_model_name()
            sql = "SELECT table_name FROM INFORMATION_SCHEMA.TABLES \
                WHERE table_name NOT IN ({}) \
                AND table_name != 'sysdiagrams' \
                AND table_name != 'date_dimension' \
                AND table_name NOT LIKE '%_daily' \
                AND table_name NOT LIKE '%_current' \
                AND table_name NOT LIKE '%_monthly' \
                AND table_name NOT LIKE '%_weekly' \
                AND table_name NOT LIKE '%_intraday' ORDER BY TABLE_NAME ASC".format(
                    ",".join("'{}'".format(table) for table in default))
        else:
            sql = "select column_name, ordinal_position \
                from INFORMATION_SCHEMA.COLUMNS \
                WHERE table_name = '%s' and ordinal_position != 1 \
                and column_name != '%s_status_id' \
                and column_name not in ('source_table', 'source_id', 'date_dimension_id') \
                ORDER BY ordinal_position ASC" % (table_name, table_name)
        sql_result = db.engine.execute(sql)
        db.session.close()
        return jsonify(data=[dict(data) for data in sql_result])