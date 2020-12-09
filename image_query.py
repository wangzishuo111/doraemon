# -*- coding: utf-8 -*- 

from base.log import *
import os
import json
import requests
import urllib2

def poc_hbase_url(trackId,trackPointId,type1,seq,imageType):
        url = 'http://10.11.5.36:8888/image/get?trackPointId=%s&type=%s&seq=%s&imageType=%s&trackId=%s' %(trackPointId,type1,seq,imageType,trackId)
        url_status = requests.get(url)
        return url_status.headers['Content-Type']

def poc_krs_url(trackId,trackPointId,type1,seq,imageType):
        url = 'http://10.11.5.34:13100/krs/image/get?trackPointId=%s&type=%s&seq=%s&imageType=%s&trackId=%s' %(trackPointId,type1,seq,imageType,trackId)
        url_status = requests.get(url)
        return url_status.headers['Content-Type']

def zw_hbase_url(trackId,trackPointId,type1,seq,imageType):
        url = 'http://10.11.5.115:8888/image/get?trackPointId=%s&type=%s&seq=%s&imageType=%s&trackId=%s' %(trackPointId,type1,seq,imageType,trackId)
        url_status = requests.get(url)
        return url_status.headers['Content-Type']

def zw_krs_url(trackId,trackPointId,type1,seq,imageType):
        url = 'http://10.11.5.74:13100/krs/image/get?trackPointId=%s&type=%s&seq=%s&imageType=%s&trackId=%s' %(trackPointId,type1,seq,imageType,trackId)
        url_status = requests.get(url)
        return url_status.headers['Content-Type']

def all_url(trackId,trackPointId,type1,seq,imageType):
        poc_hbase = poc_hbase_url(trackId,trackPointId,type1,seq,imageType)
        poc_krs = poc_krs_url(trackId,trackPointId,type1,seq,imageType)
        zw_hbase = zw_hbase_url(trackId,trackPointId,type1,seq,imageType)
        zw_krs = zw_krs_url(trackId,trackPointId,type1,seq,imageType)
        url_dict = {}
        url_dict['poc_hbase'] = poc_hbase
        url_dict['poc_krs'] = poc_krs
        url_dict['zw_hbase'] = zw_hbase
        url_dict['zw_krs'] = zw_krs
        url_json = json.dumps(url_dict)
        return url_json


def main():
	a = poc_hbase_url('13771_20180616140548806', '13771_20180616140624142515', '00', '004', 'jpg')
        b = poc_krs_url('13771_20180616140548806', '13771_20180616140624142515', '00', '004', 'jpg')
        c = zw_hbase_url('13771_20180616140548806', '13771_20180616140624142515', '00', '004', 'jpg')
        d = zw_krs_url('13771_20180616140548806', '13771_20180616140624142515', '00', '004', 'jpg')
        e = all_url('13771_20180616140548806', '13771_20180616140624142515', '00', '004', 'jpg')
        print a
        print b
        print c
        print d
        print e


if __name__ == '__main__':
	main()
