from flask_restful import Resource
from backend_api.app.common.api_utils import ApiUtils
from backend_api.app.common.db_utils import DatabaseUtils


class BlacklistApi(Resource):

    api_utils = ApiUtils()
    db_utils = DatabaseUtils()
    def post(self):
        args = self.api_utils.parameters_without_model(poller_config='append')
        
        for poller_element in args['poller_config']:
            poller_config = eval(poller_element)

        return args