# encoding: utf-8
import os
import time
import pymongo
import mongo_operator

db = mongo_operator.MongoOperator(
    '10.11.5.137',
    17000,
    'bj_test_version_management',
    'service_version')
server_list = ["autohdmap_multi_merge_cli", "test_lane_client", "autohdmap_multi_groundsymbol_client", "autohdmap_multisign_client"]
new_server_list = ["pole", "ground", "auto", "fusion"]
test_server_list = ["autohdmap_lane", "autohdmap_mutilan"] 

def set(service_name, service_version):
    insert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    item = {}
    item['service_name'] = service_name
    item['service_version'] = service_version
    item['insert_time'] = insert_time
    find_item = db.collection.find_one({'service_name': service_name, 'service_version': service_version})
    if not find_item is None:
        res = db.collection.find_one_and_replace(find_item, item)
        if not res:
            return False
        return True
    else:
        res = db.insert(item)
        if not res:
            return False
        return True

def default_set(stage, default_version):
    insert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    item = {}
    item['stage'] = service_name
    item['default_version'] = service_version
    item['insert_time'] = insert_time
    find_item = db.collection.find_one({'service_name': service_name, 'service_version': service_version})
    if not find_item is None:
        res = db.collection.find_one_and_replace(find_item, item)
        if not res:
            return False
        return True
    else:
        res = db.insert(item)
        if not res:
            return False
        return True

def get(service_name):
    item = {}
    inner_item = []
    for i in db.collection.find({'service_name': service_name}).sort("insert_time", pymongo.DESCENDING).limit(10):
        inner_item.append(i['service_version'])
    item[service_name] = inner_item
    return item

def get_all():
    item = {}
    for i in range(len(server_list)):
        inner_item = []
        for j in db.collection.find({'service_name': server_list[i]}).sort("insert_time", pymongo.DESCENDING).limit(10):
            inner_item.append(j['service_version'])
        item[server_list[i]] = inner_item
    return item


def api_main():
    data = set("autohdmap_lane","v1.0.0")
    print data
    return
    data = get("autohdmap_lane")
    print data
    return
    data = set("autohdmap_lane","v1.11.2")
    print data
    data = get_one("autohdmap_lane","v1.0.3")
    print data
    data = db.collection.distinct("service_version",{"service_name":"autohdmap_lane"}).sort("service_version", pymongo.DESCENDING).limit(10)
    print data
    data = get('autohdmap_lane')
    print data
    data = get_all()
    print data
    set('autohdmap_mutilan','v1.1.1')
    data = get('autohdmap_lane')
    print data

if __name__ == '__main__':
    api_main()
