#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys
from base.log import *
from control_lane import get_container_name as lane_get_container_name
from control_multilane import get_container_name as multilane_get_container_name
import paramiko

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

def calculate_md5sum(instance_id):
	port = 22
	user = 'kddev'
	password = 'Kuan123-deng'
	ssh = paramiko.SSHClient()
	ssh.load_system_host_keys()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	host_ip, app_name, docker_port = instance_id.split(':')
	segs = app_name.split('-')
	automap_type = segs[2]
	if automap_type == 'lane':
		container_name = lane_get_container_name(docker_port)
	elif automap_type == 'multilane':
		container_name = multilane_get_container_name(docker_port)
	ssh.connect(host_ip, port, username=user, password=password)
	if not container_name:
		assert False, 'Not found instance %s' % instance_id 
	stdin, stdout, stderr = ssh.exec_command('docker exec %s md5sum /data/CI/autohdmap_%s/autohdmap_%s_server' % (container_name, automap_type, automap_type))
	return stdout.readlines()

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
		md5 = calculate_md5sum(instance_id)		
		logger().info('checking %s', instance_id)
		if version != expect_version:
			logger().info('check %s failed, version mismatch', instance_id)
			mismatch_list.append(instance_id)
		else:
			logger().info('check %s success', instance_id)
		logger().info('check %s md5sum %s', instance_id, md5)
	logger().info('checked instance num %d', len(instance_id_list))
	return mismatch_list

def main():
	app_id = sys.argv[1]
	version = sys.argv[2]
	log_init('info', './check_automap_version_v2.txt', quiet = False)
	res = check_ver(app_id, version)
	logger().info('mismatch list %s', res)

if __name__ == '__main__':
	main()
