# -*- coding: utf-8 -*- 

from base.log import *
import os
from multiprocessing import Process
import redis_pool


def gen_id():
	r = redis_pool.get('dornaemon')
	return r.incr('deploy_id')

def do(image_name, deploy_id):
	log_path = 'html/deploy_logs/%d.txt' % deploy_id
	cmd = """ansible-playbook -i /home/op/cheng/autohdmap_deploy/production \
              /home/op/cheng/autohdmap_deploy/reco_release.yml -e 'reco_image=%s' \
              >%s 2>&1 """ % (image_name, log_path)
	logger().info('cmd:%s', cmd)
	if 0 != os.system(cmd):
		msg = '[Finish] Failed to deploy [%s]' % image_name
	else:
		msg = '[Finish] Success to deploy [%s]' % image_name
	logger().error(msg)
	open(log_path, 'a').write(msg)

def start(image_name):
	deploy_id = gen_id()
	p = Process(target=do, args=(image_name, deploy_id))
	p.start()
	logger().info('start deploy [%s]', image_name)
	return deploy_id

def status(deploy_id):
	log_path = 'html/deploy_logs/%s.txt' % deploy_id
	content = open(log_path).read()
	return content
	
def main():
	deploy_id= start('123')
	print deploy_id
	while True:
		time.sleep(1)
	#	print status(deploy_id)

if __name__ == '__main__':
	main()
