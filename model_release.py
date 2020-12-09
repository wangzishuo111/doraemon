#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from base.log import *
import os
from multiprocessing import Process
import redis_pool


def gen_id():
	r = redis_pool.get('dornaemon')
	return r.incr('deploy_id')

def do(model_name,deploy_id):
	log_path = 'html/deploy_logs/%d.txt' % deploy_id
	cmd = '/bin/bash /opt/doraemon/model-release.sh %s >> %s 2>&1' % (model_name, log_path)
	logger().info('cmd:%s', cmd)
	if 0 != os.system(cmd):
		msg = '[Finish] Failed to check [%s]' % model_name
	else:
		msg = '[Finish] Success to check [%s]' % model_name 
	logger().error(msg)
	open(log_path, 'a').write(msg)

def start(model_name):
	deploy_id = gen_id()
	p = Process(target=do, args=(model_name,deploy_id))
	p.start()
	logger().info('start check [%s]', model_name)
	return deploy_id
	
def main():
	deploy_id = start('1229347')
	while True:
		time.sleep(1)
		#print status(deploy_id)

if __name__ == '__main__':
	main()
