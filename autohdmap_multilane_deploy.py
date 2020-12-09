# -*- coding: utf-8 -*- 

from base.log import *
import os
from multiprocessing import Process
import redis_pool

def gen_id():
	r = redis_pool.get('dornaemon')
	return r.incr('deploy_id')

def do(ver, image_name, deploy_id, register_url='http://192.168.5.34:33900/'):
	log_path = 'html/deploy_logs/%d' % deploy_id
	print '%s %s %s' % (ver, image_name,log_path)
	cmd = "ansible-playbook -i /home/op/autohdmap_multilane_ma/zhangwentao " \
        "/home/op/autohdmap_multilane_ma/autohdmap_multilane.yml -t release " \
        "-e 'autohdmap_multilane_ver=%s' " \
        "-e 'autohdmap_multilane_image_name=%s' " \
        "-e 'autohdmap_multilane_register_url=%s'  >%s 2>&1" \
	% (ver, image_name, register_url, log_path)
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
	log_path = 'html/deploy_logs/%s' % deploy_id
	content = open(log_path).read()
	return content

def main():
	deploy_id = start('4.6.8', 'op-01.gzproduction.com/autohdmap/autohdmap_multilane:v1.7.1')
	while True:
		time.sleep(1)
		#print status(deploy_id)

if __name__ == '__main__':
	main()
