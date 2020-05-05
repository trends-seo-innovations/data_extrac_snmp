from enum import Enum

class sql_templates(Enum):
    poller_config = """SELECT name as poll_name,ip_address,subnet,community_string,interval,table_name 
        from snmp_poller where id = {{poll_id | sqlsafe}}"""

    oid_config = """select soid.oid_key ,ooid.oid from selected_oid soid
            left join oid_list ooid on soid.oid_key = ooid.oid_key
            where snmp_poller_id = '{{poll_id | sqlsafe}}' and ooid.brand_name = '{{brand | sqlsafe}}'"""

    poll_update_up ="""UPDATE {0} SET {1},datetime = GETDATE(),status = '1' where ip_address = '{2}' """

    poll_update_down ="""UPDATE {0} SET datetime = GETDATE(),status = '0' where ip_address = '{1}' """

    poll_insert = """Insert Into {0} ({1}) Values ({2})"""

    update_event = """UPDATE snmp_poller SET status = {{status | sqlsafe}} WHERE id = {{id | sqlsafe}}"""

    oid_prev = """SELECT oid_key ,oid from oid_list where brand_name = '{{brand | sqlsafe}}' and oid_key = '{{oid_key | sqlsafe}}'"""