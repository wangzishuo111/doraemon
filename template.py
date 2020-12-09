# -*- coding:utf-8 -*-

import sys
import time
from base.log import *

def find_repeat_begin(content, pos):
	try:
		beg = content.index('[[repeat', pos)
	except Exception, e:
		beg = -1
	if beg == -1:
		return None, None, None
	try:
		end = content.index('begin]]', beg)
	except Exception, e:
		end = -1
	assert end != -1
	
	repeat_tag = content[beg + len('[[repeat'): end].strip()[2:-2]
	last = end + len('begin]]')

	return repeat_tag, beg, last

def find_repeat_end(content, pos):
	try:
		beg = content.index('[[repeat', pos)
	except Exception, e:
		beg = -1
	if beg == -1:
		return None, None, None
	try:
		end = content.index('end]]', beg)
	except Exception, e:
		end = -1
	assert end != -1
	
	repeat_tag = content[beg + len('[[repeat'): end].strip()[2:-2]

	last = end + len('end]]')


	return repeat_tag, beg, last

class TextSeg():
	def __init__(self, text):
		self.__text = text
		self.__result = text

	def replace(self, key, value):
		key = '[[%s]]' % key
		logger().debug('replace: [%s] -> [%s]', key, value)
		while key in self.__result:
			new_result = self.__result.replace(key, value)
			#print len(new_result), ' vs ', len(self.__result)
			self.__result = new_result

	def get_text(self):
		return self.__text

	def dump(self):
		return self.__result

	def info(self):
		s = 'text: len(%d)' % len(self.__text)
		return s

class RepeatSeg():
	def __init__(self, name, text):
		self.__name = name
		self.__text = text
		self.__result = ''

	def add(self, key, value):
		one = self.__text.replace('[[%s]]' % key, value)
		self.__result += one + '\n'

	def add_ex(self, kv_map):
		text = self.__text
		for key, value in kv_map.items():
			text = text.replace('[[%s]]' % key, value)
		self.__result += text + '\n'

	def get_name(self):
		return self.__name

	def dump(self):
		return self.__result

	def info(self):
		s = 'repeat:' + self.__text
		return s
		
	
def split(content):
	pos = 0
	segs = []
	while True:
		tag, beg_start_pos, beg_end_pos = find_repeat_begin(content, pos)
		if not tag and not beg_start_pos:
			break
		#print >> sys.stderr, 'beg_pos:%d tag:%s' % (beg_start_pos, tag)
		text = content[pos:beg_start_pos]
		segs.append(TextSeg(text))

		tag, end_start_pos, end_end_pos = find_repeat_end(content, beg_end_pos)
		#print >> sys.stderr, 'beg_pos:%d tag:%s' % (end_start_pos, tag)
		repeat_content = content [beg_end_pos : end_start_pos].strip()
		#print >> sys.stderr, 'content:', repeat_content

		segs.append(RepeatSeg(tag, repeat_content))

		pos = end_end_pos

	segs.append(TextSeg(content[pos:]))
	return segs

class Manager():
	def __init__(self, content):
		self.__segs = split(content)

	def replace(self, idx, key, value):
		self.__segs[idx].replace(key, value)

	def add(self, idx, key, value):
		self.__segs[idx].add(key, value)


	def dump(self):
		ret = ''
		for seg in self.__segs:
			ret += seg.dump() + '\n'
		return ret

class ManagerV2():
	def __init__(self, content):
		self.__segs = split(content)
		self.__repeat_segs = {}
		self.__template = ''
		for seg in self.__segs:
			if isinstance(seg, RepeatSeg):
				self.__repeat_segs[seg.get_name()] = seg
				self.__template += '[[%s]]' % seg.get_name()
		
			elif isinstance(seg, TextSeg):
				self.__template += seg.get_text()

		self.__big_seg = TextSeg(self.__template)

	def replace(self, key, value):
		self.__big_seg.replace(key, value)

	def add(self, seg_name, key, value):
		self.__repeat_segs[seg_name].add(key, value)

	def add_ex(self, seg_name, kv_map):
		self.__repeat_segs[seg_name].add_ex(kv_map)

	def dump(self):
		for seg in self.__repeat_segs.values():
			cont = seg.dump()
			self.__big_seg.replace(seg.get_name(), cont)
		return self.__big_seg.dump()
			
def main():
	mgr = ManagerV2(open('./template.html').read())
	mgr.replace('name', 'cuiyanliang')
	html = mgr.dump()
	#print len(html)


if __name__ == '__main__':
	main()
