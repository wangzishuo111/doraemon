# -*- coding: utf-8 -*- 

from base.log import *
import os
from multiprocessing import Process
import redis_pool

def gen_id():
	r = redis_pool.get('dornaemon')
	return r.incr('deploy_id')

def do(ver, image_name, deploy_id, register_url='http://192.168.5.34:33900/', container_name='autohdmap_multilane', server_port='20700', cpu_num='4'):
	log_path = 'html/deploy_logs/%d.txt' % deploy_id
	print '%s %s %s %s %s %s %s' % (log_path, ver, image_name, register_url, container_name, server_port, cpu_num)
	cmd = "ansible-playbook -i /home/op/autohdmap_deploy_v2/production " \
        "/home/op/autohdmap_deploy_v2/autohdmap_multilane.yml -t release " \
        "-e 'autohdmap_multilane_ver=%s autohdmap_multilane_image_name=%s autohdmap_multilane_register_url=%s' " \
        "-e 'autohdmap_multilane_server_port=%s autohdmap_multilane_container_name=%s autohdmap_multilane_cpu_num=%s' >%s 2>&1" \
	% (ver, image_name, register_url, server_port, container_name, cpu_num, log_path)
	logger().info('cmd:%s', cmd)
	if 0 != os.system(cmd):
		msg = '[Finish] Failed to deploy [%s]' % image_name
	else:
		msg = '[Finish] Success to deploy [%s]' % image_name
	logger().error(msg)
	open(log_path, 'a').write(msg)

def start(ver, image_name):
	deploy_id = gen_id()
	p = Process(target=do, args=(ver, image_name, deploy_id))
	p.start()
	logger().info('start deploy [%s]', image_name)
	return deploy_id

def status(deploy_id):
	log_path = 'html/deploy_logs/%s.txt' % deploy_id
	content = open(log_path).read()
	return content

def main():
	deploy_id = start('4.6.8', 'op-01.gzproduction.com/autohdmap/autohdmap_multilane:v1.7.1')
	while True:
		time.sleep(1)
		#print status(deploy_id)

if __name__ == '__main__':
	main()
