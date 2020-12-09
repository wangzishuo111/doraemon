# encoding: utf-8

import mongo_operator

db = mongo_operator.MongoOperator(
    '10.11.5.137',
    17000,
    'doraemon',
    'history_operation')

def insert_operation(
        task_id,
        task_name,
        task_practitioners,
        start_time,
        end_time,
        time_consuming,
        task_status,
        ):
    item = {}
    item['task_id'] = task_id
    item['task_name'] = task_name
    item['task_practitioners'] = task_practitioners
    item['task_start_time'] = start_time
    item['task_end_time'] = end_time
    item['time_consuming'] = time_consuming
    item['task_status'] = task_status
    return db.insert(item)

def get_one_operation(task_id):
    item = db.collection.find_one({'task_id': task_id})
    return item

def get_all_operation():
    item = []
    for i in db.find():
        item.append(i)
    return item

if __name__ == '__main__':
    #for i in range(1,10):
    #insert_operation("test",'10.11.5.137:KSS-AUTOMAP-MULTILANE:20550','majiankun','1234','1235','1','True')
    #all = get_all_operation()
    #print all
    data = get_all_operation()
    for i in reversed(data):
        print i
