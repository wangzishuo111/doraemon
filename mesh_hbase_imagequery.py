# -*- coding: utf-8 -*- 

from base.log import *
import os


def get_url(trackId,trackPointId,type1,seq,imageType):
	cmd = 'http://10.11.5.115:8888/image/get?trackPointId=%s&type=%s&seq=%s&imageType=%s&trackId=%s' %(trackPointId,type1,seq,imageType,trackId)
	return cmd

def main():
	url = get_url('123', '123', '00', '004', 'jpg')
	print url

if __name__ == '__main__':
	main()
