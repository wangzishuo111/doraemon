# -*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
from base.log import *
import base.opt as opt
import sys
import base.util
import cat_helper
from singleton import *
import json


opt.add_option("-g", "--get",
               action="store_true",
               dest="get", default=False,
               help="Whether to support get methord")


def make_error_result(msg):
    ret = {}
    ret['status'] = 'fail'
    ret['msg'] = msg
    return json.dumps(ret)


def make_success_result(k=None, v=None):
    ret = {}
    ret['status'] = 'success'
    if k:
        ret[k] = v
    return json.dumps(ret)


class FileHandler(tornado.web.RequestHandler):
    def get(self):
        path = self.request.path
        if path.startswith('/'):
            path = path[1:]

        localpath = os.path.join('html', path + '.html')
        html = open(localpath).read()
        self.write(html)


class BaseHandler(tornado.web.RequestHandler):

    def set_json_result(self, data):
        self.write(data)
        self.set_header('Content-type', 'application/json')

    def save_file(self, path, name):
        paths = []
        for k, v in self.request.files.items():
            print k, v[0].filename

            filename = v[0].filename
            filename = util.transcode(filename)
            suffix = util.get_suffix(filename)

            full_path = os.path.join(path, str('%s%s' % (name, suffix)))

            logger().info('save file %s', full_path)
            with open(full_path, 'wb') as up:
                up.write(v[0]['body'])
            up.close()
            paths.append(full_path)
        return paths

    def process(self):
        logger().error('not implement')
        sys.exit(-1)

    def get(self):
        cat_helper.agent_reset()
        try:
            if opt.option().get:
                return self.process()
            else:
                msg = 'get method not supported'
                logger().error(msg)
                self.write(msg)
                self.set_status(404)
        finally:
            cat_helper.agent_finish()

    def post(self):
        cat_helper.agent_reset()
        try:
            self.process()
        finally:
            cat_helper.agent_finish()

    def get_arg(self, key):
        return self.get_argument(key).encode('utf-8')

    def get_arg_ex(self, key, dft_val):
        try:
            val = self.get_argument(key)
            if val.strip() == 'null':
                val = None
            if not val:
                return dft_val
            if isinstance(val, unicode):
                val = val.encode('utf-8')
            return val
        except BaseException:
            return dft_val

    def get_current_user(self):
        return self.get_secure_cookie("Username")


def main():
    pass


if __name__ == '__main__':
    main()
