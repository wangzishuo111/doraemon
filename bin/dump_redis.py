#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import redis

redis_utils = redis.Redis(host='10.11.5.114', password='kdgogo', port=6379, db=13)
service = 'automation'

def dump_redis_info():
    all_info_to_show = '\n-------------- 运行中的 automation 任务:' + str(redis_utils.scard("automation_running")) + '------------\n'
    all_info_to_show += '\n-------------- 队列中的 automation 任务 ' + str(redis_utils.llen("automation_cmd_start_queue")) + ' ------------\n'
    
    return all_info_to_show



    
def main():
    print dump_redis_info()

if __name__ == '__main__':
    main()
