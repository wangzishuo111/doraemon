#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from base.log import *
import os
from multiprocessing import Process
import redis_pool


def gen_id():
	r = redis_pool.get('dornaemon')
	return r.incr('deploy_id')

def dostart():
	#log_path = 'html/deploy_logs/%d.txt' % int(deploy_id)
	cmd = 'ssh hadoop@hadoop-0021 /bin/bash /home/hadoop/qihongjiang/info.csv.sh >> /tmp/info_csv.log 2>&1' 
	logger().info('cmd:%s', cmd)
	if 0 != os.system(cmd):
		msg = '[Finish] Failed to release info.csv ' 
		tag = False
	else:
		msg = '[Finish] Success to release info.csv '
		tag = True
	logger().error(msg)
	return tag
	#open(log_path, 'a').write(msg)

#def start():
#	#deploy_id = gen_id()
#	p = Process(target=do)
#	p.start()
#	logger().info('info.csv start release')
#	return 	

def main():
	deploy_id = start('1229347')
	while True:
		time.sleep(1)
		#print status(deploy_id)

if __name__ == '__main__':
	main()
