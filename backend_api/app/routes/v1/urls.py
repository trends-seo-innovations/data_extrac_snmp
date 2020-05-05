from backend_api.app.api import api
from backend_api.app import app
from backend_api.app.api.test_api import TestApi
from backend_api.app.api.login_api import LoginApi
from backend_api.app.api.accounts_api import AccountsApi
from backend_api.app.api.authentication_api import AuthenticationApi
from backend_api.app.api.extractor_api import ExtractorApi
from backend_api.app.api.worker_api import WorkerApi
from backend_api.app.api.extractresponse_api import ExtractResponse
from backend_api.app.api.normalize_api import NormalizeApi
from backend_api.app.api.schema_api import SchemaAPI
from backend_api.app.api.workerservice_api import WorkerService
from backend_api.app.api.aggregator_api import AggregatorApi
from backend_api.app.api.aggregateservice_api import AggregateService

api.add_resource(TestApi, '/api/v1/testapi')
api.add_resource(LoginApi, '/api/v1/login/auth')
api.add_resource(AccountsApi, '/api/v1/account', '/api/v1/account/<int:id>')

api.add_resource(AuthenticationApi, '/api/v1/authentication', '/api/v1/authentication/<int:id>')

api.add_resource(ExtractorApi, '/api/v1/extractor', '/api/v1/extractor/<int:id>')
api.add_resource(ExtractResponse, '/api/v1/extract/response')

api.add_resource(WorkerApi, '/api/v1/worker', '/api/v1/worker/<int:id>')
api.add_resource(WorkerService, '/api/v1/worker/service', '/api/v1/worker/service/<int:id>',
    '/api/v1/worker/service/<int:id>/logs', '/api/v1/worker/service/<int:id>/logs/<string:level>')

api.add_resource(NormalizeApi, '/api/v1/normalize', '/api/v1/normalize/<int:id>')
api.add_resource(SchemaAPI, '/api/v1/schema/tables' ,'/api/v1/schema/tables/<string:table_name>/columns')

api.add_resource(AggregatorApi, '/api/v1/aggregate', '/api/v1/aggregate/<int:id>', '/api/v1/aggregate/<int:id>/<string:attribute>')
api.add_resource(AggregateService, '/api/v1/aggregate/service', '/api/v1/aggregate/service/<int:id>', 
    '/api/v1/aggregate/service/<int:id>/logs', '/api/v1/aggregate/service/<int:id>/logs/<string:level>')


