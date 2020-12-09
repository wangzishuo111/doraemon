# encoding: utf-8

import mongo_operator

db = mongo_operator.MongoOperator(
    '10.11.5.137',
    17000,
    'parallel_service',
    'test')

def insert_operation(
        server,
        version,
	insert_time
        ):
    db_name = '%s_tab' %server
    db = mongo_operator.MongoOperator(
        '10.11.5.137',
        17000,
        'parallel_service',
        db_name)
    item = {}
    item['server'] = server 
    item['version'] = version
    item['insert_time'] = insert_time
    return db.insert(item)


def get_all_version():
    db_name = 'server_version'
    db = mongo_operator.MongoOperator(
        '10.11.5.137',
        17000,
        'parallel_service',
        db_name)
    item = []
    for i in db.find().sort([('server', 1), ('insert_time', 1)]):
        item.append(i)
    return item

if __name__ == '__main__':
   # insert_operation('autohdmap_lane', 'v8')
    print get_all_version('autohdmap_lane')
    #for i in range(1,10):
    #insert_operation("test",'10.11.5.137:KSS-AUTOMAP-MULTILANE:20550','majiankun','1234','1235','1','True')
    #all = get_all_operation()
    #print all
  #  data = get_all_operation()
  #  for i in reversed(data):
  #      print i
