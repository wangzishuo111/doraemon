# -*- coding:utf-8 -*-

import os
from HTMLParser import HTMLParser
import time

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
	HTMLParser.__init__(self)
	self.__one_data = {}
	self.__data = []
	self.__key = None
        
    def handle_starttag(self, tag, attrs):
	if tag == 'dd':
		attrs = dict(attrs)	
		if 'class' in attrs :
			self.__key = attrs['class']

	if self.__key == 'img' and tag == 'img':
		src = dict(attrs)['src']
		self.__one_data['img'] = src

    def handle_endtag(self, tag):
	if self.__key:
		self.__key = None
	if len(self.__one_data) == 6:
		'''
		for k, v in self.__one_data.items():
			print k, v
		print
		'''
		self.__data.append(self.__one_data)
		self.__one_data = {}


    def handle_data(self, data):
	if self.__key:
		if data.endswith('级'):
			self.__one_data['wind'] = data
			return
 		if self.__key not in self.__one_data:
			self.__one_data[self.__key] = ''
		self.__one_data[self.__key] += data

		#print self.__key
		#print len(self.__one_data)
                

    def dump(self):
	return self.__data

# instantiate the parser and fed it some HTML

def wget():
	date = time.strftime("%Y%m%d")
	path = os.path.join('./weather', date)
	if not os.path.exists(path):
		cmd = 'wget "https://www.tianqi.com/beijing/7/" -O %s' % path
		os.system(cmd)

	content = open(path).read()
	return content

def get_data():
	content = wget()
	parser = MyHTMLParser()
	parser.feed(content)
	return parser.dump()

def main():
	get_data()

	'''
partly-cloudy-day
clear-day
snow
partly-cloudy-night
cloudy
fog




'''

	

if __name__ == '__main__':
	main()
