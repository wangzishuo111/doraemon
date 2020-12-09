# -*- coding: utf-8 -*- 

from base.log import *
import os
from multiprocessing import Process
import redis_pool

def gen_id():
	r = redis_pool.get('dornaemon')
	return r.incr('deploy_id')

def do(service_name, version, oprate_item, deploy_id):
	log_path = 'html/deploy_logs/%d.txt' % deploy_id
	print '%s' % (log_path)
	cmd = "sudo ansible-playbook -i /home/op/Java_service_release/host_list /home/op/Java_service_release/Java_service_release.yml -t %s -f 10 -e service_name=%s -e version=%s  >%s 2>&1" % (oprate_item, service_name,version, log_path)
	print cmd
	logger().info('cmd:%s', cmd)
	if 0 != os.system(cmd):
		msg = '[Finish] Failed to start  [%s]' % deploy_id
	else:
		msg = '[Finish] Success to start [%s]' % deploy_id
	logger().error(msg)
	open(log_path, 'a').write(msg)

def start(service_name, version, oprate_item):
	deploy_id = gen_id()
	p = Process(target=do, args=(service_name, version, oprate_item, deploy_id,))
	p.start()
	logger().info('start deploys [%s]',deploy_id)
	return deploy_id

def status(deploy_id):
	log_path = 'html/deploy_logs/%s.txt' % deploy_id
	content = open(log_path).read()
	return content

def main():
	deploy_id = start("krs","1", "start")
	while True:
		time.sleep(1)
		#print status(deploy_id)

if __name__ == '__main__':
	main()
