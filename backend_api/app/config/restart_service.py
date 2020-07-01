
from backend_api.app.models.snmp_poller import SnmpPoller
from backend_api.app.models.snmp_poller_schema import SnmpPollerSchema
from backend_api.app.common.api_utils import ApiUtils
from backend_api.app.common.db_utils import DatabaseUtils
from backend_api.app.common.service_manager import ServiceManager
import sys


api_utils = ApiUtils()
db_utils = DatabaseUtils()


if 'no_service' not in sys.argv:
    poll_service = ServiceManager(module_name='poller')
    poller_service = db_utils.select_with_filter(SnmpPoller, SnmpPollerSchema, {'status': 1})
    # poll_service.restart_service(poller_service, 'poller.exe')
    poll_service.restart_service(poller_service, 'poller.py')
    
