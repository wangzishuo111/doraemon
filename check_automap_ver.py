#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys
from base.log import *

def from_eureka_get_svc(app_id, eureka_url='http://srv-10.gzproduction.com:13900/eureka/apps'):
	url = eureka_url + '/' + app_id
	headers = {'accept': 'application/json'}
	res = requests.get(url, headers=headers)
	if not res:
		return None
	try:
		jdata = res.json()
	except Exception,e:
		assert False, 'No Json decoded'
	instance_list = jdata.get('application').get('instance')
	formated_instance = []
	for instance in instance_list:
		formated_instance.append(instance.get('instanceId'))
	return formated_instance

def get_version(instance_id):
	host_ip, app_name, port = instance_id.split(':')
	instance_url = 'http://%s:%s/%s/info' % (host_ip, port, app_name)
	try:
		res = requests.get(instance_url)
		jdata = res.json()
	except Exception, e:
		import traceback
		print traceback.format_exc()
	ver = jdata.get('version')
	return ver

def check_ver(app_id, expect_version):
	instance_id_list = from_eureka_get_svc(app_id=app_id)
	mismatch_list = []
	if not instance_id_list:
		return []
	for instance_id in instance_id_list:
		version = get_version(instance_id)
		logger().info('checking %s', instance_id)
		if version != expect_version:
			logger().info('check %s failed, version mismatch', instance_id)
			mismatch_list.append(instance_id)
		else:
			logger().info('check %s success', instance_id)
	return mismatch_list	

def main():
	app_id = sys.argv[1]
	version = sys.argv[2]
	log_init('info', './check_automap_version.txt', quiet = False)
	res = check_ver(app_id, version)
	logger().info('mismatch list %s', res)

if __name__ == '__main__':
	main()
