# encoding: utf-8
'''
@author: mjk
@file: mongo_operator.py
@time: 2018/11/4 11:11
@desc: 
'''

import pymongo as pm
import json

class MongoOperator:
    def __init__(self, host, port, db_name, collection):
        '''
        设置mongodb的地址，端口以及默认访问的集合，后续访问中如果不指定collection，则访问这个默认的
        :param host: 地址
        :param port: 端口
        :param db_name: 数据库名字
        :param default_collection: 默认的集合
        '''
        #建立数据库连接
        self.client = pm.MongoClient(host=host, port=port, connect=False)
        #选择相应的数据库名称
        self.db = self.client.get_database(db_name)
        #设置默认的集合
        self.collection = self.db.get_collection(collection)

    def insert(self, item, collection_name =None):
        '''
        插入数据，这里的数据可以是一个，也可以是多个
        :param item: 需要插入的数据
        :param collection_name:  可选，需要访问哪个集合
        :return:
        '''
        if collection_name != None:
            collection = self.db.get_collection(collection_name)
            return collection.insert(item)
        else:
            return self.collection.insert(item)

    def find(self, expression =None, collection_name=None):
        '''
        进行简单查询，可以指定条件和集合
        :param expression: 查询条件，可以为空
        :param collection_name: 集合名称
        :return: 所有结果
        '''
        if collection_name != None:
            collection = self.db.get_collection(collection_name)
            if expression == None:
                return collection.find()
            else:
                return collection.find(expression)
        else:
            if expression == None:
                return self.collection.find()
            else:
                return self.collection.find(expression)

    def remove(self, item, collection_name =None):
        '''
        删除数据，这里的数据可以是一个，也可以是多个
        :param item: 需要删除的数据
        :param collection_name:  可选，需要访问哪个集合
        :return:
        '''
        if collection_name != None:
            collection = self.db.get_collection(collection_name)
            collection.remove(item)
        else:
            self.collection.remove(item)

    def get_collection(self, collection_name=None):
        '''
        很多时候单纯的查询不能够通过这个类封装的方法执行，这时候就可以直接获取到对应的collection进行操作
        :param collection_name: 集合名称
        :return: collection
        '''
        if collection_name == None:
            return self.collection
        else:
            return self.get_collection(collection_name)

if __name__ == '__main__':
    db = MongoOperator('10.11.5.137', 17000, 'version_management', 'service_version')
    data = db.collection.find({'service_name': "autohdmap_lane", 'service_version': "v3.2.3"})
    print type(data)
    item = []
    for i in db.collection.find({'service_name': "autohdmap_lane", 'service_version': "v3.2.3"}):
        item = i.read()
    print item
    if item is None:
        print "this is null"
    #find_item = {"service_name": "autohdmap_lane","service_version": "v1.0.3"}
    #print type(find_item)
    #replace_item = {"service_name": "autohdmap_lane","service_version": "v1.0.3","insert_time" : "2019-02-12 11:10:44"}
    #print type(replace_item)
    #db.collection.find_one_and_replace(find_item, replace_item)
