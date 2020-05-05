from backend_api.app.api import api
from backend_api.app.api.kpi_data import KpiData
from backend_api.app.api.kpi_api import KpiApi
from backend_api.app.api.dataset_api import DataSetApi
from backend_api.app.api.category_api import CategoryApi
from backend_api.app.api.icons_api import IconsApi

api.add_resource(KpiApi, '/api/v2/kpi', '/api/v2/kpi/<int:id>')
api.add_resource(KpiData, '/api/v2/kpi/data/<string:table_name>')

api.add_resource(DataSetApi, '/api/v2/datasets', '/api/v2/datasets/<int:id>')

api.add_resource(CategoryApi, '/api/v2/categories', '/api/v2/categories/<int:id>')
api.add_resource(IconsApi, '/api/v2/icons', '/api/v2/icons/<int:id>')