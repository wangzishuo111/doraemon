#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from base.log import *
import os
from multiprocessing import Process
import redis_pool


def gen_id():
	r = redis_pool.get('dornaemon')
	return r.incr('deploy_id')

def do(task_id, deploy_id):
	log_path = 'deploy_logs/%d' % deploy_id
	cmd = 'bash /home/op/cheng/hbase-store/find_005_09.sh %s > %s 2>&1' % (task_id, log_path)
	logger().info('cmd:%s', cmd)
	if 0 != os.system(cmd):
		msg = '[Finish] Failed to check [%s]' % task_id
	else:
		msg = '[Finish] Success to check [%s]' %  task_id
	logger().error(msg)
	open(log_path, 'a').write(msg)

def start(task_id):
	deploy_id = gen_id()
	p = Process(target=do, args=(task_id, deploy_id))
	p.start()
	logger().info('start check [%s]', task_id)
	return deploy_id

def status(deploy_id):
	log_path = 'deploy_logs/%s' % deploy_id
	content = open(log_path).read()
	return content
	
def main():
	deploy_id = start('1229347')
	while True:
		time.sleep(1)
		#print status(deploy_id)

if __name__ == '__main__':
	main()
