# -*- coding: utf-8 -*-
from base.log import *
import os
from multiprocessing import Process
import redis_pool

def gen_id():
	r = redis_pool.get('dornaemon')
	return r.incr('deploy_id')

def do(deploy_id):
	log_path = 'html/deploy_logs/%d' % deploy_id
	cmd = "ansible -i /home/op/autohdmap_multilane_ma/production all " \
	"-m shell -a " \
	"'docker exec -i autohdmap_multilane_0 md5sum /data/CI/autohdmap_multilane/autohdmap_multilane_server ;docker exec -i autohdmap_multilane_1 md5sum /data/CI/autohdmap_multilane/autohdmap_multilane_server' -f 100 >%s 2>&1" \
	% (log_path)
	logger().info('cmd:%s', cmd)
	if 0 != os.system(cmd):
		msg = '[Finish] Failed to Check Version' 
	else:
		msg = '[Finish] Check Version Succeed'
	logger().error(msg)
	open(log_path, 'a').write(msg)
#close方法
#	with open("a.txt") as f:
#		sxxxxxx
#	f.close()


def start():
	deploy_id = gen_id()
	p = Process(target=do, args=(deploy_id,))
	p.start()
	logger().info('start check version')
	return deploy_id

def status(deploy_id):
	log_path = 'html/deploy_logs/%s' % deploy_id
	content = open(log_path).read()
	return content

def main():
	deploy_id = start()
	while True:
		time.sleep(1)

if __name__ == '__main__':
	main()
