from flask_restful import Resource
from backend_api.app.common.api_utils import ApiUtils
from backend_api.app.common.db_utils import DatabaseUtils

from backend_api.app.models.snmp_poller import SnmpPoller
from backend_api.app.models.snmp_poller_schema import SnmpPollerSchema
class BlacklistApi(Resource):

    api_utils = ApiUtils()
    db_utils = DatabaseUtils()
    main_model = SnmpPoller
    def post(self):
        conn = DatabaseUtil(os.environ.get("DB_CONN"), os.environ.get("DB_USER"), os.environ.get("DB_PASSWORD"), os.environ.get("DB_NAME"))
        args = self.api_utils.parameters(self.main_model(), blacklist="append", selected_oid="append", ip_list="append")
       
        # args = self.api_utils.parameters_without_model(poller_config='append')
        # for poller_element in args['poller_config']:
        #     poller_config = eval(poller_element)
        
        return args