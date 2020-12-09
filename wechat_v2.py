#!/usr/bin/python
# -*- coding: utf-8 -*-
# zabbix notification confirmation script
  
import requests
import json
import os
import sys
from base.log import *
  
AgentID = 1000003 
CropID = 'ww507937ab80780fe4'
Secret = 'KlSxzyoWMlAy4fjYLvboVadV8Ft8xfyWuZ0lrYdvGRc'
Gtoken ="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid="+ CropID + "&corpsecret=" + Secret
headers = {'Content-Type': 'application/json'}

def get_token():
    ret = requests.get(Gtoken)
    res = ret.json()
    logger().debug('res[%s]', res)
    if not res['errcode'] == 0:
        return None
    return res['access_token']

  
def msg(title, message, Toparty):
    token = get_token()
    Purl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token
    weixin_msg = {
         "toparty" : Toparty,
         "msgtype" : "text",
         "agentid" : AgentID,
         "text" : {
             "content": "%s\n%s" % (title, message)
          }
      }
    ret = requests.post(Purl, json.dumps(weixin_msg), headers=headers)
    logger().info('wechat return %s', ret.json())
    return 0 == ret.json()['errcode']
  
if __name__ == '__main__':
    title = sys.argv[1]  
    message = sys.argv[2] 
    Toparty = sys.argv[3]
    print msg(title,message, Toparty)
