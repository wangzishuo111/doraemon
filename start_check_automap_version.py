# -*- coding: utf-8 -*- 

from base.log import *
import os
from multiprocessing import Process
import redis_pool


def gen_id():
	r = redis_pool.get('dornaemon')
	return r.incr('deploy_id')

def do(app_id, version, deploy_id):
	log_path = 'html/deploy_logs/%d.txt' % deploy_id
	cmd = 'python check_automap_ver_v2.py %s %s > %s 2>&1' % (app_id, version, log_path)
	logger().info('cmd:%s', cmd)
	if 0 != os.system(cmd):
		msg = '[Finish] Failed to check [%s]' % app_id
	else:
		msg = '[Finish] Success to check [%s]' % app_id
	logger().error(msg)
	open(log_path, 'a').write(msg)

def start(app_id, version):
	deploy_id = gen_id()
	p = Process(target=do, args=(app_id, version, deploy_id))
	p.start()
	logger().info('start check [%s]', app_id)
	return deploy_id

def status(deploy_id):
	log_path = 'html/deploy_logs/%s.txt' % deploy_id
	content = open(log_path).read()
	return content
	
def main():
	deploy_id = start('kss-automap-lane', 'v4.7.4')
	while True:
		time.sleep(1)
		#print status(deploy_id)

if __name__ == '__main__':
	main()
