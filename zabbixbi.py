#!/usr/bin/python
# encoding: utf-8


import datetime
import time
import csv
import json
from datetime import datetime, timedelta
from pyzabbix import ZabbixAPI


def login_zabbix(zabbix_url, username, password):
    zapi = ZabbixAPI(zabbix_url)
    zapi.login(username, password)
    return zapi


def get_host_list(zapi, groupid):
    groups_info = zapi.host.get(groupids=groupid, sortfield='host')
    host_list = []
    for i in range(len(groups_info)):
        host_info = {}
        host_info['name'] = groups_info[i]['name']
        host_info['host'] = groups_info[i]['host']
        host_info['hostid'] = groups_info[i]['hostid']
        host_list.append(host_info)
    return host_list


def get_item_list(host_list, key_list, zapi):
    item_list = []
    for i in range(len(host_list)):
        for key in range(len(key_list)):
            item_list.append(zapi.item.get(hostids=host_list[i]['hostid'], search={u'key_': key_list[key]}))
    return item_list


def get_valueinfo(host_list, item_list, zapi,date_today,time_till,time_from):
    #print date_today,time_till,time_from
    for i in range(len(host_list)):
        value = {}
        for j in range(len(item_list)):
            # 这里加一个判断列表是否为空，或者在前面就给空列表去掉
            if item_list[j] != [] and host_list[i]['hostid'] == item_list[j][0]['hostid']:
                value_hours = zapi.trend.get(itemids=item_list[j][0]['itemid'], output=['value_avg'],
                                             time_from=time_from, time_till=time_till)  # 24小时的值
                sum = 0
                value_avg = 0
                for m in range(len(value_hours[0:16])):
                    sum += float(value_hours[m]['value_avg'])
                value_avg = round(sum / 16, 4)
                value[item_list[j][0]['key_'].encode('ascii')] = str(value_avg)
        value["hostname"] = host_list[i]['name']
        value["date"] = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        data = json.dumps(value)
        print(data)


def main():
    date_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timetuple()
    time_till = time.mktime(date_today)
    time_from = time_till - 60 * 60 * 16
    #print time.strftime('%Y-%m-%d',time.localtime(time.time()))
    key_list = ['system.cpu.util[,user]','vm.memory.size[total]', 'vm.memory.size[available]',
                'gpu.utilisation[0]', 'gpu.utilisation[1]', 'gpu.utilisation[2]', 'gpu.utilisation[3]',
                 'net.if.out[bond0]','net.if.in[bond0]']

    zapi = login_zabbix("http://op-01.gzproduction.com:8082/zabbix", "majiankun", "Kdtemp02")

    host_list = get_host_list(zapi, "17")
    host_list = host_list
    item_list = get_item_list(host_list, key_list, zapi)
    get_valueinfo(host_list, item_list, zapi,date_today,time_till,time_from)



if __name__ == '__main__':
    main()


