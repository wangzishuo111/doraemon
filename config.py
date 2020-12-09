# -*- coding:utf-8 -*

import ConfigParser
from singleton import *

@singleton
class __Manager():
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read("conf.ini")

    def get_ex(self, name, key, dft_val):
        try:
            return self.cf.get(name, key)
        except Exception, e:
            print e
            return dft_val

    def get(self, name, key):
        return self.cf.get(name, key)


def GET_CONF_EX(name, key, dft_val):
    manager = __Manager()
    return manager.get_ex(name, key, dft_val)

def GET_CONF(name, key):
    manager = __Manager()
    return manager.get(name, key)


def main():
    print GET_CONF_EX('avg_click_computer', 'hit_key_name', None)
    print GET_CONF_EX('db1', 'db_host', None)
    print GET_CONF_EX('db', 'db_host1', None)

if __name__ == '__main__':
    main()
