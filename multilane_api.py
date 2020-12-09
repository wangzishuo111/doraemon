# -*- coding: utf-8 -*- 

from base.log import *
import os
from multiprocessing import Process
import redis_pool

def gen_id():
	r = redis_pool.get('dornaemon')
	return r.incr('deploy_id')


def doversion(deploy_id):
	log_path = 'html/deploy_logs/%d.txt' % deploy_id
	print '%s' % (log_path)
	cmd = "bash /home/op/autohdmap_multilane_ma/check_multilane_version.sh >%s 2>&1" % (log_path)
	print cmd
	logger().info('cmd:%s', cmd)
	if 0 != os.system(cmd):
		msg = '[Finish] Failed to CheckVersion [%s]' % deploy_id
	else:
		msg = '[Finish] Success to CheckVersion [%s]' % deploy_id
	logger().error(msg)
	open(log_path, 'a').write(msg)

def version():
	deploy_id = gen_id()
	p = Process(target=doversion, args=(deploy_id,))
	p.start()
	logger().info('start deploys [%s]',deploy_id)
	return deploy_id


def doclean(deploy_id):
	log_path = 'html/deploy_logs/%d.txt' % deploy_id
	print '%s' % (log_path)
	cmd = "ansible-playbook -i  /home/op/autohdmap_multilane_ma/production /home/op/autohdmap_multilane_ma/clean_task.yml -f 100 >%s 2>&1" % (log_path)
	print cmd
	logger().info('cmd:%s', cmd)
	if 0 != os.system(cmd):
		msg = '[Finish] Failed to clean [%s]' % deploy_id
	else:
		msg = '[Finish] Success to clean [%s]' % deploy_id
	logger().error(msg)
	open(log_path, 'a').write(msg)

def clean():
	deploy_id = gen_id()
	p = Process(target=doclean, args=(deploy_id,))
	p.start()
	logger().info('start deploys [%s]',deploy_id)
	return deploy_id


def dorestart():
	log_path = 'html/deploy_logs/autohdmap_multilane_restart.txt'
	cmd = "ansible-playbook -i /home/op/autohdmap_multilane_ma/production /home/op/autohdmap_multilane_ma/autohdmap_multilane.yml -t restart -f 100 >%s 2>&1" % (log_path)
	#cmd = "ansible-playbook -i /home/op/autohdmap_multilane_ma/test /home/op/autohdmap_multilane_ma/mjk_test.yml -t restart -f 100 >%s 2>&1" % (log_path)
	logger().info('cmd:%s', cmd)
	if 0 != os.system(cmd):
		msg = '[Finish] Failed to restart'
		tag = False
	else:
		msg = '[Finish] Success to restart'
		tag = True
	logger().error(msg)
	open(log_path, 'a').write(msg)
	return tag


def dostop():
	log_path = 'html/deploy_logs/autohdmap_multilane_stop.txt'
	cmd = "ansible-playbook -i /home/op/autohdmap_multilane_ma/production autohdmap_multilane.yml -t stop -f 100 >%s 2>&1" % (log_path)
	#cmd = "ansible-playbook -i /home/op/autohdmap_multilane_ma/test /home/op/autohdmap_multilane_ma/mjk_test.yml -t stop -f 100 >%s 2>&1" % (log_path)
	logger().info('cmd:%s', cmd)
	if 0 != os.system(cmd):
		msg = '[Finish] Failed to stop' 
		tag = False
	else:
		msg = '[Finish] Success to stop' 
		tag = True
	logger().error(msg)
	open(log_path, 'a').write(msg)
	return tag


def dostart():
	log_path = 'html/deploy_logs/autohdmap_multilane_start.txt'
	cmd = "ansible-playbook -i /home/op/autohdmap_multilane_ma/production /home/op/autohdmap_multilane_ma/autohdmap_multilane.yml -t start -f 100 >%s 2>&1" % (log_path)
	#cmd = "ansible-playbook -i /home/op/autohdmap_multilane_ma/test /home/op/autohdmap_multilane_ma/mjk_test.yml -t start -f 100 >%s 2>&1" % (log_path)
	logger().info('cmd:%s', cmd)
	if 0 != os.system(cmd):
		msg = '[Finish] Failed to start all ' 
		tag = False
	else:
		msg = '[Finish] Success to start all ' 
		tag = True
	logger().error(msg)
	open(log_path, 'a').write(msg)
	return tag

def status(deploy_id):
	log_path = 'html/deploy_logs/%s.txt' % deploy_id
	content = open(log_path).read()
	return content

def main():
	deploy_id = start()
	while True:
		time.sleep(1)
		#print status(deploy_id)

if __name__ == '__main__':
	main()
