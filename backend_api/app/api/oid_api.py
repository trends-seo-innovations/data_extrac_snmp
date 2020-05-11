from flask_restful import Resource
from flask_restful import reqparse
from backend_api.app.api import db
from flask_jwt_extended import jwt_required
from backend_api.app.common.api_utils import ApiUtils
from backend_api.app.common.db_utils import DatabaseUtils
from backend_api.app.models.oid_list import OidList
from backend_api.app.models.oid_list_schema import OidListSchema

class OidApi(Resource):
    

    api_utils = ApiUtils()
    db_utils = DatabaseUtils()

    main_model = OidList
    main_schema = OidListSchema

    @jwt_required

    def get(self, id=None):
        oid_list = db.session.query(self.main_model.oid_key).distinct(self.main_model.oid_key)
        if id is not None:
            oid_list = oid_list.filter(self.main_model.id==id)
        print(oid_list)
        oid_list.all()
        oid_result = self.main_schema(many=True).dump(oid_list)
        return {'data': oid_result}, 200