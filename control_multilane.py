#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko
import scpclient
from contextlib import closing
import os
import sys
import time
import requests
from base.log import *


# 10.11.5.44:KSS-AUTOMAP-LANE:20527

def control_container(ip, container_port, action):
	port = 22 
	user = 'kddev'
	password = 'Kuan123-deng'
	ssh = paramiko.SSHClient()
	ssh.load_system_host_keys()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	container_name = get_container_name(container_port)
	logger().info("host[%s] container_name[%s] action[%s]", ip, container_name, action)
	ssh.connect(ip, port, username=user, password=password)
	if action == 'restart':
        	stdin, stdout, stderr = ssh.exec_command('docker exec %s /bin/bash -C /data/CI/autohdmap_multilane/autohdmap_multilane.sh stop' % container_name)
		time.sleep(0.5)
        	stdin, stdout, stderr = ssh.exec_command('docker exec %s /bin/bash -C /data/CI/autohdmap_multilane/autohdmap_multilane.sh start' % container_name)
	elif action == 'stop':
        	stdin, stdout, stderr = ssh.exec_command('docker exec %s /bin/bash -C /data/CI/autohdmap_multilane/autohdmap_multilane.sh stop' % container_name)
	elif action == 'start':
        	stdin, stdout, stderr = ssh.exec_command('docker exec %s /bin/bash -C /data/CI/autohdmap_multilane/autohdmap_multilane.sh start' % container_name)
	else:
		assert False, "Not support action!!!"

def get_container_name(port):
	port_name_mapping = {
		'20550': 'autohdmap_multilane_0',
		'20551': 'autohdmap_multilane_1',
	}
	return port_name_mapping.get(port)

def check_instance_status(instance_id):
	host_ip, service_name, port = instance_id.split(':')
	url = 'http://%s:%s/%s/info' % (host_ip, port, service_name.lower())
	ret = requests.get(url)
	try:
		res = ret.json()
	except Exception, e:
		res = None
		logger().error('autohdmap return not Json')
	return res.get('status') == 'UP', res

def control_multilane(instance_id, action):
	host_ip, service_name, port = instance_id.split(':')
	control_container(host_ip, port, action=action)
	if action != 'stop':
		# after control service, wait a moment
		time.sleep(0.5)
		status, response = check_instance_status(instance_id)
	# If action is stop, skip check instance status
	else:
		status, response = True, 'success'
	return status, response

def main(instance_id, action):
	status, response = control_multilane(instance_id, action)
	print status, response

if __name__ == '__main__':
	log_init('info', './log.txt', quiet = False)
	instance_id = sys.argv[1]
	action = sys.argv[2]
	main(instance_id, action)
