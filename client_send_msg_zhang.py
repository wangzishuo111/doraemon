#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base.log import *
import requests

def send_msg(title, message):
	send_msg_url = 'http://op-01.gzproduction.com:9527/api/msg/send'
	payload = {'title': title, 'message': message}
	ret = requests.get(send_msg_url, params=payload)
	print ret
	return '0' == ret.json()['code']

if __name__ == '__main__':
	try:
		s = send_msg("zhang","wentao")
	except Exception, e:
		logger().error('retry send ')
		s = send_msg("zhang","wentao")
