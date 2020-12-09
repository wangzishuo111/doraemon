# -*- coding: utf-8 -*- 

from base.log import *
import os
from multiprocessing import Process
import redis_pool

def gen_id():
	r = redis_pool.get('dornaemon')
	return r.incr('deploy_id')

def do(host_name, deploy_id):
	log_path = 'html/deploy_logs/%d.txt' % deploy_id
	cmd = "python /home/op/mesh_deploy_5.80/clear_lane.py %s > %s 2>&1" % (host_name, log_path)
	logger().info('cmd:%s', cmd)
	if 0 != os.system(cmd):
		msg = '[Finish] Failed to deploy [%s]' % deploy_id
	else:
		msg = '[Finish] Success to deploy [%s]' % deploy_id
	logger().error(msg)
	open(log_path, 'a').write(msg)

def start(host_name):
	deploy_id = gen_id()
	p = Process(target=do, args=(host_name, deploy_id))
	p.start()
	logger().info('start deploy [%s]', deploy_id)
	return deploy_id

def status(deploy_id):
	log_path = 'html/deploy_logs/%s.txt' % deploy_id
	content = open(log_path).read()
	return content

def main():
	deploy_id = start('mongo-02')
	while True:
		time.sleep(1)
		#print status(deploy_id)

if __name__ == '__main__':
	main()
