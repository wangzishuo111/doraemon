# -*- coding:utf-8 -*-

import cat

from base.log import *
from singleton import *


@singleton
class CatInit():
    def __init__(self):
        logger().info('cat init')
        cat.init("kd.hbase")


@singleton
class CatStage():
    def __init__(self):
        CatInit()
        self.__stage_map = {}

    def stage_begin(self, space, name):
        key = (space, name)
        name = '%s/%s' % (space, name)
        self.__stage_map[key] = cat.Transaction(space, name)

    def stage_end(self, space, name):
        key = (space, name)
        name = '%s/%s' % (space, name)
        self.__stage_map[key].complete()
        del self.__stage_map[key]


@singleton
class CatStageAgency():
    def __init__(self):
        CatInit()
        self.reset()

    def reset(self):
        self.__stage_map = {}

    def stage_begin(self, space, name):
        key = (space, name)
        name = '%s/%s' % (space, name)
        self.__stage_map[key] = cat.Transaction(space, name)

    def finish(self):
        for val in self.__stage_map.values():
            val.complete()
        self.__stage_map = {}

# ----------------Shortcut--------------


def stage_begin(space, name):
    CatStage().stage_begin(space, name)


def stage_end(space, name):
    CatStage().stage_end(space, name)


def agent_stage_begin(space, name):
    CatStageAgency().stage_begin(space, name)


def agent_reset():
    CatStageAgency().reset()


def agent_finish():
    CatStageAgency().finish()


def log_event(space, name):
    name = '%s/%s' % (space, name)
    cat.log_event(space, name)


def test():
    import time
    stage_begin('a', 'b')
    stage_begin('a', 'c')
    time.sleep(1)
    stage_end('a', 'b')
    stage_end('a', 'c')


def main():
    import time
    agent_reset()
    agent_stage_begin('a', 'b')
    agent_stage_begin('a', 'c')
    time.sleep(2)
    agent_finish()
    log_event('test', 'a')


if __name__ == '__main__':
    main()
