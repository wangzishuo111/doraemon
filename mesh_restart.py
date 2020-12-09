# -*- coding: utf-8 -*- 

from base.log import *
import os
from multiprocessing import Process
import redis_pool

def gen_id():
	r = redis_pool.get('dornaemon')
	return r.incr('deploy_id')

def do_start(server_name, deploy_id):
	log_path = 'html/deploy_logs/%d.txt' % deploy_id
	cmd = "cat /home/op/mesh_deploy_5.80/%s | python /home/op/mesh_deploy_5.80/guizhou_start.py > %s 2>&1" % (server_name, log_path)
	logger().info('cmd:%s', cmd)
	if 0 != os.system(cmd):
		msg = '[Finish] Failed to deploy [%s]' % deploy_id
	else:
		msg = '[Finish] Success to deploy [%s]' % deploy_id
	logger().error(msg)
	open(log_path, 'a').write(msg)

def do_stop(server_name, deploy_id):
	log_path = 'html/deploy_logs/%d.txt' % deploy_id
	cmd = "cat /home/op/mesh_deploy_5.80/%s | python /home/op/mesh_deploy_5.80/guizhou_stop.py > %s 2>&1" % (server_name, log_path)
	logger().info('cmd:%s', cmd)
	if 0 != os.system(cmd):
		msg = '[Finish] Failed to deploy [%s]' % deploy_id
	else:
		msg = '[Finish] Success to deploy [%s]' % deploy_id
	logger().error(msg)
	open(log_path, 'a').write(msg)

def do_restart(server_name, deploy_id):
	log_path = 'html/deploy_logs/%d.txt' % deploy_id
	cmd = "cat /home/op/mesh_deploy_5.80/%s | python /home/op/mesh_deploy_5.80/guizhou_restart.py > %s 2>&1" % (server_name, log_path)
	logger().info('cmd:%s', cmd)
	if 0 != os.system(cmd):
		msg = '[Finish] Failed to deploy [%s]' % deploy_id
	else:
		msg = '[Finish] Success to deploy [%s]' % deploy_id
	logger().error(msg)
	open(log_path, 'a').write(msg)

def start(server_name):
	deploy_id = gen_id()
	p = Process(target=do_start, args=(server_name, deploy_id))
	p.start()
	logger().info('start deploy [%s]', deploy_id)
	return deploy_id

def stop(server_name):
	deploy_id = gen_id()
	p = Process(target=do_stop, args=(server_name, deploy_id))
	p.start()
	logger().info('start deploy [%s]', deploy_id)
	return deploy_id

def restart(server_name):
	deploy_id = gen_id()
	p = Process(target=do_restart, args=(server_name, deploy_id))
	p.start()
	logger().info('start deploy [%s]', deploy_id)
	return deploy_id

def enter(server_name, oprate_item):
	if oprate_item == 'start':
		deploy_id = start(server_name)
		return deploy_id
	elif oprate_item == 'stop':
		deploy_id = stop(server_name)
		return deploy_id
	elif oprate_item == 'restart':
		deploy_id = restart(server_name)
		return deploy_id
	else:
		assert False, 'your enter a wrong item'

def main():
	deploy_id = enter('kpms', 'start')
	print deploy_id
	while True:
		time.sleep(1)

if __name__ == '__main__':
	main()
