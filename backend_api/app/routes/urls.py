from backend_api.app.api import api



from backend_api.app.api.snmppoller_api import SnmpPollerApi
from backend_api.app.api.pollerservice_api import PollerService
from backend_api.app.api.blacklist_api import BlacklistApi
from backend_api.app.api.oid_api import OidApi
from backend_api.app.api.datapolling_api import DataPollingApi
from backend_api.app.api.poller_data import PollerData
from backend_api.app.api.poller_status import PollerStatus

from backend_api.app.api.networkdiscovery_api import NetworkDiscovery


api.add_resource(SnmpPollerApi, '/snmp/poller', '/snmp/poller/<int:id>')
api.add_resource(PollerService, '/poller/service', '/poller/service/<int:id>', 
    '/poller/service/<int:id>/logs', '/poller/service/<int:id>/logs/<string:level>')
api.add_resource(BlacklistApi, '/blacklist')
api.add_resource(OidApi, '/oid')
api.add_resource(NetworkDiscovery, '/network/discovery')
api.add_resource(DataPollingApi, '/data/view/polling')
api.add_resource(PollerData, '/poller/data', '/poller/data/<string:table_name>')
api.add_resource(PollerStatus, '/poller/status', '/poller/status/<string:table_name>')

