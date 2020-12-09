# -*- coding:utf-8 -*-
import httplib
import json
import urllib
import urllib2
import sys
import os
import time

from timer import Timer
import httplib

conn = httplib.HTTPConnection("localhost:9527")


def write(batch, seq, data):
	url = '/kds/data/task/123/auto/edit?batch=%s&seq=%s' % (batch, seq)
	conn.request(method="POST", url=url, body=data)

	response = conn.getresponse()
	res_data = response.read()
	status = response.status
	print status
	print res_data
	print '--'

def read(batch):
	url = '/kds/data/batch/%s/auto/query' % (batch)
	conn.request(method="GET", url=url)

	response = conn.getresponse()
	res_data = response.read()
	status = response.status
	print status
	print res_data

def delete(seq):
	url = '/kds/data/seq/%s/auto/delete' % (seq)
	conn.request(method="GET", url=url)

	response = conn.getresponse()
	res_data = response.read()
	status = response.status
	print status
	print res_data


def main():
	data = json.dumps({'1': '2'})
	print write('123_2', '12312', data)
	print read('123_2')
	print delete('123_2-123_1')
	print read('123_2')

if __name__ == '__main__' :
	main()
