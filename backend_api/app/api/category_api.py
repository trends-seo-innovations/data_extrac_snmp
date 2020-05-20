from flask_restful import Resource
from flask_restful import reqparse
from backend_api.app.api import db
from flask_jwt_extended import jwt_required
from backend_api.app.common.api_utils import ApiUtils
from backend_api.app.common.db_utils import DatabaseUtils
from backend_api.app.models.categories import Categories
from backend_api.app.models.categories_schema import CategoriesSchema

class CategoryApi(Resource):
    

    api_utils = ApiUtils()
    db_utils = DatabaseUtils()

    main_model = Categories
    main_schema = CategoriesSchema

    
    def get(self, id=None):
        category = db.session.query(self.main_model)
        if id is not None:
            category = category.filter(self.main_model.id==id)
        category.all()
        category_result = self.main_schema(many=True).dump(category)
        return {'data': category_result}, 200