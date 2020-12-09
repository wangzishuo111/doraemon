# -*- coding:utf-8 -*-

from HTMLParser import HTMLParser

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
#        print "Encountered a start tag:", tag

    def handle_endtag(self, tag):
	if self.__key:
		self.__key = None
	if len(self.__one_data) == 4:
		for k, v in self.__one_data.items():
			print k, v
		print
		self.__data.append(self.__one_data)
		self.__one_data = {}


    def handle_data(self, data):
	if self.__key:
		if self.__key not in self.__one_data:
			self.__one_data[self.__key] = ''
		self.__one_data[self.__key] += data
		#print self.__key
		#print len(self.__one_data)
                

    def dump():
	pass

# instantiate the parser and fed it some HTML

def main():
	parser = MyHTMLParser()
	parser.feed(open('weather.html').read())
	

if __name__ == '__main__':
	main()
