# encoding: utf-8
'''
@author: mjk
@file: user.py
@time: 2018/11/4 11:06
@desc: 
'''

import json
import time
import mongo_operator
db = mongo_operator.MongoOperator('10.11.5.137', 17000, 'doraemon', 'user')
now_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))



def user_add(username,showname,password,user_group,encryption):
    item = {}
    item['username'] = username
    item['showname'] = showname
    item['password'] = password
    item['user_group'] = user_group
    item['encryption'] = encryption
    item['create_time'] = now_date
    return db.insert(item)


def user_remove(username,password):
    item = {}
    item['username'] = username
    item['password'] = password
    return db.remove(item)


def user_info(username):
    item = db.collection.find_one({'username':username})
    return item

def user_login(username,password):
    userinfo = user_info(username)
    if username == userinfo['username'] and password == userinfo['password']:
        print userinfo['username'],userinfo['password'],userinfo['encryption']
        if "op" == userinfo['user_group'] and "7ef05292a28940d59ff780510c323c8b" == userinfo['encryption'] :
            return userinfo['user_group']
        elif "kd" == userinfo['user_group'] and "" == userinfo['encryption']:
            return userinfo['user_group']
        elif "test" == userinfo['user_group'] and "" == userinfo['encryption']:
            return userinfo['user_group']
        elif "pm" == userinfo['user_group'] and "" == userinfo['encryption']:
            return userinfo['user_group']
    else:
        return False

def match_name(username):
    userinfo = user_info(username)
    if username == userinfo['username']:
        showname = userinfo['showname']
    else:
        showname = username['username']
    return showname

if __name__ == '__main__':
   # user_add('majiankun','马建坤','wozuiyaobai','op','7ef05292a28940d59ff780510c323c8b')
   # user_add('zhangwentao','张文涛','wozuiyaobai','op','7ef05292a28940d59ff780510c323c8b')
   # user_add('qihongjiang','齐洪江','wozuiyaobai','op','7ef05292a28940d59ff780510c323c8b')
   # user_add('wangzishuo','王子硕','wozuiyaobai','op','7ef05292a28940d59ff780510c323c8b')
   # user_add('shencheng','沈城','wozuiyaobai','op','7ef05292a28940d59ff780510c323c8b')
   # user_add('cuiyanliang','老大','wozuiyaobai','op','7ef05292a28940d59ff780510c323c8b')
   # user_add('haoweiliang','郝卫亮','wozuiyaobai','op','7ef05292a28940d59ff780510c323c8b')
   # user_add('liuhao','刘浩','wozuiyaobai','op','7ef05292a28940d59ff780510c323c8b')
   # user_add('qizongqing','齐综擎','wozuiyaobai','op','7ef05292a28940d59ff780510c323c8b')
   #user_add('chengyoumei','程有美','wozuiyaobai','op','7ef05292a28940d59ff780510c323c8b')
   user_add('hexiaoan','何潇安','wozuiyaobai','op','7ef05292a28940d59ff780510c323c8b')
    #user_add('other','other','','','7ef05292a28940d59ff780510c323c8b')
    #result = db.collection.find_one({'username':'majiankun'})
    #a = json.loads(result)
    #print a['username']
    #user_remove('wangjing','jiejiezuimei')
    #flag =  user_login('majiankun','Kdtemp02')
    #print flag
    #name = match_name('other')
    #print name
