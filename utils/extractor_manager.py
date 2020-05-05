from utils.database_util import DatabaseUtil
from requests.auth import HTTPBasicAuth
from backend_api.app.models.error_schema import ErrorObject
import requests
import json
import re
requests.packages.urllib3.disable_warnings()



class ExtractorManager():

    def __init__(self, auth=None, args=None):
        self.auth = auth[0]
        self.args = args

    def authentication(self):
        try:
            if self.args['type'] == "API":
                if self.auth['authentication_type'] == 'token':
                    url = "{0}{1}".format(self.auth['host'], self.auth['token_url'])
                    auth = requests.post(url, auth=HTTPBasicAuth(username=self.auth['username'], 
                        password=self.auth['password']), verify=False)
                    return auth.json()
                else:
                    return None
            elif self.args['type'] == "Database":
                conn = DatabaseUtil(self.auth['host'], self.auth['username'], 
                    self.auth['password'], self.auth['db_name'])
                test_conn = conn.get_connection(api=True)
                return conn
        except Exception as err:
            raise ValueError('Cannot connect to source {0} - {1}'.format(self.args['type'], self.auth['host']))

    def set_parameters(self):
        if self.args['type'] == "API":
            parameter = {}
            for param in self.args['parameter']:
                param = eval(param)
                if param['param_type'] != 'url':
                    parameter[param['key']] = param['value']
            return parameter
        elif self.args['type'] == "Database":
            params = ""
            if self.args['parameter']:
                params = " WHERE {0}".format(' AND '.join('{0} =  \'{1}\''.format(eval(param)['key'], eval(param)['value']) 
                    for param in self.args['parameter']))
            return params

    def data(self, no_limit=None):
        try:
            auth = self.authentication()
            parameter = self.set_parameters()
           
            if self.args['type'] == "API":
                if self.auth['authentication_type'] == 'token':

                    api_url = "{0}{1}".format(self.auth['host'], self.args['url'])
                    target_api = requests.request(self.args['method'], api_url, headers={ self.auth['token_header']: auth['Token'] }, 
                        params=parameter,verify=False)
                    status_code = target_api.status_code
                    if status_code == 401 or status_code == 403 \
                        or status_code == 400 or status_code == 404:
                        raise ValueError("Invalid url or method")
                    return target_api.json()
                else:
                    api_url = "{0}{1}".format(self.auth['host'], self.args['url'])
                    
                    for param in self.args['parameter']:
                        param = eval(param)
                        if param['param_type'] == 'url':
                            api_url = '{0}/{1}'.format(api_url, param['value'])

                    target_api = requests.request(self.args['method'], api_url, headers={ self.auth['token_header']: self.auth['password'] }, 
                        params=parameter,verify=False)
                    status_code = target_api.status_code
                    if status_code == 401 or status_code == 403 \
                        or status_code == 400 or status_code == 404:
                        raise ValueError("Invalid url or method")
                    return {
                        '0': target_api.json()
                    }
            elif self.args['type'] == "Database":
                for param in self.args['parameter']:
                    param = eval(param)

                 # add top 1 in query
                query = self.args['url']
                if self.args['get_values']:
                    select_word = 'select'
                    select_index = query.lower().find(select_word)
                    if select_index != -1:
                        validate_line = query[select_index + 1:]
                        top_word = 'top 1'
                        top_index = validate_line.lower().find(top_word)
                        if top_index <= 0:
                            index = select_index + len(select_word)   
                            query = query[:index] + ' TOP 5' + query[index:]

                if no_limit:
                    query_string = "{0} {1}".format(self.args['url'], self.set_parameters())  
                else:
                    query_string = "{0} {1}".format(query, self.set_parameters()) 
                data = auth.select_query(query_string)
                #temp
                data_cleanse = []
                data_obj = {}

                if data:
                    if no_limit:
                        return data
                    if self.args['get_values']:
                        for data_values in data:
                            for key, value in data_values.items():
                                data_obj[str(key)] = str(value)
                            data_cleanse.append(data_obj)
                        return data_cleanse
                    else:
                        for key, value in data[0].items():
                            data_obj[str(key)] = ""
                        data_cleanse.append(data_obj)
                        return data_cleanse
                else:
                    data_fields = {}
                    if "*" in self.args['url']:
                        query_set = str(self.args['url']).split(" ")
                        sql_info_schema = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME IN "
                        for i in range(len(query_set)):
                            if str(query_set[i]).lower() == 'from':
                                tables =  query_set[i+1].split(",")
                                sql_info_schema += "({}".format(",".join("'{0}'".format(table) for table in tables))
                            if str(query_set[i]).lower() == 'join':
                                sql_info_schema += ",'{}'".format(query_set[i+1])
                        sql_info_schema += ")"
                        data = auth.select_query(sql_info_schema)
                        new_dict = {} 
                        for key in data:
                            data_fields[key['column_name']] = ""
                        data_cleanse.append(data_fields)
                    else:

                        query_set = re.sub("select|SELECT|distinct|DISTINCT", "", str(self.args['url']))
                        parse_query = query_set[:str(query_set).lower().find('from')].split(",")
                        for field in parse_query:
                            remove_period = field.find(".")
                            removed_period = field[remove_period+1:]
                            final_removed = removed_period.split(" ")
                            if len(final_removed) >= 2:
                                data_fields[final_removed[2]] = ""
                            else:
                                data_fields[removed_period] = ""
                            # remove_period = field.find(".")
                            # data_fields[field[remove_period+1:]] = ""
                        data_cleanse.append(data_fields)
              
                return data_cleanse

        except ValueError as value_err:
            raise ValueError(ErrorObject(message="Encountered an error : {0}".format(value_err), type="ValueError").to_json())
        except UnicodeError as unicode_error:
            raise ValueError(ErrorObject(message="Encountered an error : {0}".format(unicode_error), type="UnicodeError").to_json())
        except requests.exceptions.ConnectionError as conn_err:
            raise ValueError(ErrorObject(message="Invalid request url or query format", type="ConnectionError").to_json())
        except Exception as err:
            raise ValueError(ErrorObject(message=str(err), type="ExceptionError").to_json())