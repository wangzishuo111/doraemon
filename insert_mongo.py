# encoding: utf-8

import mongo_operator

db = mongo_operator.MongoOperator(
    '10.11.5.137',
    17000,
    'problem',
    'problem_list')

def insert_problem(
        title,
        message,
        insert_time,
        status,
        ):
    item = {}
    item['title'] = title
    item['message'] = message
    item['insert_time'] = insert_time
    item['status'] = status 
    return db.insert(item)

def get_all_problem():
    item = []
    for i in db.find():
        item.append(i)
    return item

if __name__ == '__main__':
    #insert_operation("redis problem",'10.11.5.137 redis is dead','16.04','Error')
    data = get_all_problem()
    for i in reversed(data):
        print i
