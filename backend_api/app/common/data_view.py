from backend_api.app import db
from flask import jsonify

def data_view(args, table_name):
    if args['limit'] == 0:
        sql = 'SELECT * FROM %s' % table_name
    else: 
        sql = '''SELECT * FROM (
                SELECT ROW_NUMBER() OVER(ORDER BY %s) AS rown,
                * FROM %s
                ) tbl
                WHERE rown BETWEEN %s AND %s''' % (table_name + '_id', table_name, args['start'], args['limit'])
    sql_result = db.engine.execute(sql)
    db.session.close()
    # return jsonify(data=[dict(data) for data in sql_result])
    result = []
    for data in sql_result:
        result.append(dict(data))
    return result
