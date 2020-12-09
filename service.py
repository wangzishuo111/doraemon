# -*- coding:utf-8 -*- 
import tornado.ioloop
import tornado.web
import json
import os
import random
import time
import web_release

import tornado.httputil
import base_http
import base.opt as opt
from base import util
from base.log import *
import timer
import cat_helper
import reco_deploy
import zhang_clean_ltask
import zhang_clean_mtask
import zhang_clean_mtask
import autohdmap_lane_deploy
import autohdmap_multilane_deploy
import autohdmap_fusion_deploy
import template
import poc_java_start
import auto_java_start
import weather
import hbase_store_release
import user
import mesh_release
import mesh_restart
import multilane_version_check
import wechat
import wechat_v2
import mesh_hbase_imagequery
import image_query
import control_lane
import autohdmap_lane_start_all
import control_multilane
import autohdmap_multilane_start_all
import start_check_automap_version
import history_operation
import check_005_09
import sys
import clean_autohdmap_lane
import java_release
import hadoop_transfile
import autohdmap_api
import multilane_api
import insert_mongo
import version_control
import model_release
import info_csv 
import version_management
import bj_test_version_management
import requests
reload(sys)
sys.setdefaultencoding('utf-8')

opt.add_option("-p", "--port", dest="port", default=1973, help="service port")


def make_error_result(error, msg):
    logger().error(msg)
    ret = {}
    ret['code'] = error
    ret['message'] = msg
    ret['error'] = None
    ret['result'] = None 
    return json.dumps(ret)


def make_success_result(result=None):
    ret = {}
    ret['code'] = '0'
    ret['message'] = '成功'
    ret['error'] = None
    ret['result'] = result
    return json.dumps(ret)


def make_success_result_int(result=None):
    ret = {}
    ret['code'] = 0
    ret['message'] = '成功'
    ret['error'] = None
    ret['result'] = result
    return json.dumps(ret)

class TestHandler(base_http.BaseHandler):
    def process(self):
        #logger().info("id:%s", id(self))
        data = self.request.body
        print data
        print '===='
        for f, c in self.request.files.items():
            print f, c[0]['filename'], c[0]['body']

        '''
	for k, v in self.request.body_arguments.items():
        	self.arguments.setdefault(k, []).extend(v)
	'''

        for f, c in self.request.files.items():
            print f, c

        # for k, v in self.arguments.items():
        #	print k, v


class DashboardHandler(base_http.BaseHandler):
    def process(self):
        data = weather.get_data()
        mgr = template.ManagerV2(open('template/dashboard.html').read())
        mgr.replace('today weather', data[0]['temp'])
        mgr.replace('today temp', data[0]['txt'])
        mgr.replace('today wind', data[0]['wind'])
        image_path = os.path.join('images', os.path.basename(data[0]['img']))
        mgr.replace('today img', image_path)

        for i in range(1, len(data)):
            d = data[i]
            res = {}
            res['week'] = d['week']
            res['temp'] = d['txt']
            res['wind'] = d['wind']
            res['weather'] = d['temp']
            image_path = os.path.join('images', os.path.basename(d['img']))
            res['img'] = image_path
            mgr.add_ex('weather', res)
        html = mgr.dump()
        self.write(html)


class RecoDeployStartHandler(base_http.BaseHandler):
    def process(self):
        try:
            image_name = self.get_arg('imageName')
            username = user.match_name(self.get_arg('username'))
        except Exception as e:
            import traceback
            logger().error('bad args, query[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        start_time = time.time()
        deploy_id = reco_deploy.start(image_name)
        end_time = time.time()
        time_consuming = end_time - start_time
        start_time = timer.format_time(start_time)
        end_time = timer.format_time(end_time)
        history_operation.insert_operation(deploy_id,"hadoop集群镜像部署  "+image_name,username,start_time,end_time,time_consuming,"还没有想到怎么获取状态的值")
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)


class DeployStatusHandler(base_http.BaseHandler):
    def process(self):
        try:
            deploy_id = self.get_arg('deployId')
        except Exception as e:
            import traceback
            logger().error('bad args, query[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        content = reco_deploy.status(deploy_id)
        segs = content.split('\n')
        segs = segs[::-1]
        meta = '<meta http-equiv="refresh" content="1">'
        for i in range(len(segs)):
            seg = segs[i]
            if seg.startswith('[Finish]'):
                meta = ''
                if 'Failed' in seg:
                    seg = '<b><font size="4" color="red">%s</font></b>' % seg
                    segs[i] = seg
                else:
                    seg = '<b><font size="4" color="green">%s</font></b>' % seg
                    segs[i] = seg
            elif seg.startswith('fatal'):
                seg = '<font size="3" color="red">%s</font>' % seg
                segs[i] = seg
            elif seg.startswith('ok'):
                seg = '<font size="3" color="green">%s</font>' % seg
                segs[i] = seg
        content = '<br>'.join(segs)
        mgr = template.ManagerV2(open('./template/deploy_status.html').read())
        mgr.replace('meta', meta)
        mgr.replace('body', content)
        html = mgr.dump()
        self.write(html)

class AutoHdmapMultiLaneDeployStartHandler(base_http.BaseHandler):
    def process(self):
        try:
            ver = self.get_arg('ver')
            image_name = self.get_arg('image_name')
            username = user.match_name(self.get_arg('username'))
        except Exception as e:
            import traceback
            logger().error('bad args, query[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        start_time = time.time()
        deploy_id = autohdmap_multilane_deploy.start(ver, image_name)
        end_time = time.time()
        time_consuming = end_time - start_time
        start_time = timer.format_time(start_time)
        end_time = timer.format_time(end_time)
        history_operation.insert_operation(deploy_id,"Autohdmap_Multilane" + image_name,username,start_time,end_time,time_consuming,"还没做好如何取到状态值")
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)

class JavaServiceDeployStartHandler(base_http.BaseHandler):
    def process(self):
        try:
            release_path = self.get_arg('release_path')
        except Exception as e:
            import traceback
            logger().error('bad args, query[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        res = {}
        deploy_id = auto_java_start.start(release_path)
        # self.set_json_result(make_success_result(res))
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)


class AutoHdmapFusionDeployStartHandler(base_http.BaseHandler):
    def process(self):
        try:
            ver = self.get_arg('ver')
            image_name = self.get_arg('image_name')
        except Exception as e:
            import traceback
            logger().error('bad args, query[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        res = {}
        deploy_id = autohdmap_fusion_deploy.start(
            ver, image_name)
        # self.set_json_result(make_success_result(res))
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)

class AutoHdmapLaneDeployStartHandler(base_http.BaseHandler):
    def process(self):
        try:
            ver = self.get_arg('ver')
            image_name = self.get_arg('image_name')
            username = user.match_name(self.get_arg('username'))
        except Exception as e:
            import traceback
            logger().error('bad args, query[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        start_time = time.time()
        deploy_id = autohdmap_lane_deploy.start(ver, image_name)
        end_time = time.time()
        time_consuming = end_time - start_time
        start_time = timer.format_time(start_time)
        end_time = timer.format_time(end_time)
        history_operation.insert_operation(deploy_id,"Autohdmap_lane" + image_name,username,start_time,end_time,time_consuming,"还没做好如何取到状态值")
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)

class HbaseStoreStartHandler(base_http.BaseHandler):
    def process(self):
        username = user.match_name(self.get_arg('username'))
        start_time = time.time()
        deploy_id = hbase_store_release.start()
        end_time = time.time()
        time_consuming = end_time - start_time
        start_time = timer.format_time(start_time)
        end_time = timer.format_time(end_time)
        history_operation.insert_operation(deploy_id,"HbaseStore 部署", username,start_time,end_time,time_consuming,"还没做好如何取到状态值")
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)

class AutoInfoHandler(base_http.BaseHandler):
    def process(self):
        meta = '<meta http-equiv="refresh" content="1">'
        content = os.popen('python bin/dump_redis.py').read()
        mgr = template.ManagerV2(open('./template/redis_stat.html').read())
        mgr.replace('meta', meta)
        content = content.replace('\n', '<br>')
        mgr.replace('body', content)
        html = mgr.dump()
        self.write(html)
        
class LoginHandler(base_http.BaseHandler):
    def post(self):
        username = self.get_arg('Username')
        password = self.get_arg('Password')
        flag = user.user_login(username,password)
        print '----------------------------------->',flag
        if flag == "op":
            self.set_secure_cookie(username,'80510c323c8b')
            self.redirect('/index.html' )
        elif flag == "pm":
            self.set_secure_cookie(username,'7ef05292')
            self.redirect('/pm_index.html' )
        elif flag =="kd":
            self.set_secure_cookie(username,'7ef05292')
            self.redirect('/kd_index.html' )
        elif flag == "test":
            self.set_secure_cookie(username,'7ef05292')
            self.redirect('/test_index.html' )
        elif flag == False:
            print 'elif----------------------------------->',flag
            self.redirect('/login.html')

class LogoutHandler(base_http.BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/login.html')


class WelcomeHandler(base_http.BaseHandler):
    def get(self):
        if not self.get_secure_cookie(username):
            self.redirect('/login.html')
        else:
            self.redirect('/index.html')

class MeshReleaseStartHandler(base_http.BaseHandler):
    def process(self):
        try:
            username = user.match_name(self.get_arg('username'))
            release_path = self.get_arg('release_path')
        except Exception as e:
            import traceback
            logger().error('bad args, query[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        start_time = time.time()
        deploy_id = mesh_release.start(release_path)
        end_time = time.time()
        time_consuming = end_time - start_time
        length = release_path.find("release-data")
        release_path = release_path[length+len("release-data"):]
        start_time = timer.format_time(start_time)
        end_time = timer.format_time(end_time)
        history_operation.insert_operation(deploy_id,release_path,username,start_time,end_time,time_consuming,"还没做好如何取到状态值")
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)

class HadoopTransFileStartHandler(base_http.BaseHandler):
    def process(self):
        try:
            username = user.match_name(self.get_arg('username'))
            src_path = self.get_arg('src_path')
            dest_path = self.get_arg('dest_path')
	    file_mode = self.get_arg('file_mode')
        except Exception as e:
            import traceback
            logger().error('bad args, query[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        start_time = time.time()
        deploy_id = hadoop_transfile.start(src_path, dest_path, file_mode)
        end_time = time.time()
        time_consuming = end_time - start_time
        start_time = timer.format_time(start_time)
        end_time = timer.format_time(end_time)
        history_operation.insert_operation(deploy_id,'file_transport',username,start_time,end_time,time_consuming,"还没做好如何取到状态值")
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)




class WebReleaseStartHandler(base_http.BaseHandler):
    def process(self):
        try:
            username = user.match_name(self.get_arg('username'))
            release_path = self.get_arg('release_path')
        except Exception as e:
            import traceback
            logger().error('bad args, query[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        start_time = time.time()
        deploy_id = web_release.start(release_path)
        end_time = time.time()
        time_consuming = end_time - start_time
        length = release_path.find("release-data")
        release_path = release_path[length+len("release-data"):]
        start_time = timer.format_time(start_time)
        end_time = timer.format_time(end_time)
        history_operation.insert_operation(deploy_id,release_path,username,start_time,end_time,time_consuming,"还没做好如何取到状态值")
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)

class MeshRestartStartHandler(base_http.BaseHandler):
    def process(self):
        try:
            username = user.match_name(self.get_arg('username'))
            server_name = self.get_arg('server_name')
	    oprate_item = self.get_arg('oprate_item')
        except Exception as e:
            import traceback
            logger().error('bad args, query[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        start_time = time.time()
        deploy_id = mesh_restart.enter(server_name, oprate_item)
        end_time = time.time()
        time_consuming = end_time - start_time
        start_time = timer.format_time(start_time)
        end_time = timer.format_time(end_time)
        history_operation.insert_operation(deploy_id,server_name,oprate_item+username,start_time,end_time,time_consuming,"还没做好如何取到状态值")
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)


class MeshHbaseImageStartHandler(base_http.BaseHandler):
    def process(self):
        try:
            trackId = self.get_arg('trackId')
            trackPointId = self.get_arg('trackPointId')
            type1 = self.get_arg('type1')
            seq = self.get_arg('seq')
            imageType = self.get_arg('imageType')
        except Exception as e:
            import traceback
            logger().error('bad args, query[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return

        img_url = mesh_hbase_imagequery.get_url(trackId,trackPointId,type1,seq,imageType)
        self.redirect(img_url)


class AutohdmaplaneCleanUPStartHandler(base_http.BaseHandler):
    def process(self):
        try:
            username = user.match_name(self.get_arg('username'))
            host_name = self.get_arg('host_name')
	    print username , host_name
        except Exception as e:
            import traceback
            logger().error('bad args, query[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        start_time = time.time()
        deploy_id = clean_autohdmap_lane.start(host_name)
        end_time = time.time()
        time_consuming = end_time - start_time
        start_time = timer.format_time(start_time)
        end_time = timer.format_time(end_time)
        history_operation.insert_operation(deploy_id,host_name,username,start_time,end_time,time_consuming,"还没做好如何取到状态值")
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)

class ImageStartHandler(base_http.BaseHandler):
    def process(self):
        try:
            trackId = self.get_arg('trackId')
            trackPointId = self.get_arg('trackPointId')
            type1 = self.get_arg('type1')
            seq = self.get_arg('seq')
            imageType = self.get_arg('imageType')
        except Exception as e:
            import traceback
            logger().error('bad args, query[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        img_url = image_query.all_url(trackId,trackPointId,type1,seq,imageType)
	print '----------------------------------------------------------------->',img_url
	print '----------------------------------------------------------------->',type(img_url)
        self.write(img_url)
        #self.redirect('/index.html?img_url=%s' %(img_url) )
      #  self.redirect(img_url)

class SendMsgHandler(base_http.BaseHandler):
    def process(self):
        try:
            title = self.get_arg('title')
            message = self.get_arg('message')
            to_party = self.get_arg('to_party') 
        except Exception as e:
            import traceback
            logger().error('bad args, query[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        ##TODO 0 -> weixin; 1 -> mail 2 -> ALL
        alert_type = self.get_arg_ex('alert_type', '2')
        logger().info('title[%s] message[%s] to_party[%s]',
                      title, message[:20], to_party)
        ret = wechat.msg(title, message, to_party)
        logger().info('wechat return %s', ret)
        if ret:
            self.set_json_result(make_success_result())
            insert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            status = "ERROR"
            insert_mongo.insert_problem(title, message, insert_time, status)
            return
        else:
            self.set_json_result(make_error_result(3, 'dont send successful'))        

class SendMsgTextHandler(base_http.BaseHandler):
    def process(self):
        try:
            title = self.get_arg('title')
            message = self.get_arg('message')
            to_party = self.get_arg('to_party') 
        except Exception as e:
            import traceback
            logger().error('bad args, query[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        ##TODO 0 -> weixin; 1 -> mail 2 -> ALL
        logger().info('title[%s] message[%s] to_party[%s]',
                      title, message[:20], to_party)
        ret = wechat_v2.msg(title, message, to_party)
        logger().info('wechat_v2 return %s', ret)
        if ret:
            self.set_json_result(make_success_result())
            insert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            status = "ERROR"
            insert_mongo.insert_problem(title, message, insert_time, status)
            return
        else:
            self.set_json_result(make_error_result(3, 'dont send successful'))        

class AutoHdmapLaneOneControlHandler(base_http.BaseHandler):
    def process(self):
        try:
            instance_id = self.get_arg('instance_id')
            action = self.get_arg('action')
            username = user.match_name(self.get_arg('username'))
        except Exception as e:
            import traceback
            logger().error('bad args, query`[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        start_time = time.time()
        status, response = control_lane.control_lane(instance_id, action)
        end_time = time.time()
        time_consuming = end_time - start_time
        start_time = timer.format_time(start_time)
        end_time = timer.format_time(end_time)
        history_operation.insert_operation(instance_id,action,username,start_time,end_time,time_consuming,status)
        if status:
            self.set_json_result(make_success_result(response))
            return
        else:
            self.set_json_result(make_error_result(3, response))	

class AutoHdmapLaneAllControlHandler(base_http.BaseHandler):
    def process(self):
        username = user.match_name(self.get_arg('username'))
        start_time = time.time()
        deploy_id = autohdmap_lane_start_all.start()
        end_time = time.time()
        time_consuming = end_time - start_time
        start_time = timer.format_time(start_time)
        end_time = timer.format_time(end_time)
        history_operation.insert_operation(deploy_id,"AutoHdmapLaneAll",username,start_time,end_time,time_consuming,"还没方法取到状态")
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)

        
class AutoHdmapMultiLaneOneControlHandler(base_http.BaseHandler):
    def process(self):
        try:
            instance_id = self.get_arg('instance_id')
            action = self.get_arg('action')
            username = user.match_name(self.get_arg('username'))
        except Exception as e:
            import traceback
            logger().error('bad args, query`[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        start_time = time.time()
        status, response = control_multilane.control_multilane(instance_id, action)
        end_time = time.time()
        time_consuming = end_time - start_time
        start_time = timer.format_time(start_time)
        end_time = timer.format_time(end_time)
        history_operation.insert_operation(instance_id,action,username,start_time,end_time,time_consuming,status)
        if status:
            self.set_json_result(make_success_result(response))
            return
        else:
            self.set_json_result(make_error_result(3, response))



class JavareleaseStartHandler(base_http.BaseHandler):
    def process(self):
        try:
            service_name = self.get_arg('service_name')
            service_name = service_name.lower()
            version = self.get_arg('version')
	    oprate_item = self.get_arg('oprate_item')
            username = user.match_name(self.get_arg('username'))
        except Exception as e:
            import traceback
            logger().error('bad args, query`[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        deploy_id = java_release.start(service_name, version, oprate_item)
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)



class AutoHdmapMultiLaneAllControlHandler(base_http.BaseHandler):
    def process(self):
        username = user.match_name(self.get_arg('username'))
        start_time = time.time()
        deploy_id = autohdmap_multilane_start_all.start()
        end_time = time.time()
        time_consuming = end_time - start_time
        start_time = timer.format_time(start_time)
        end_time = timer.format_time(end_time)
        history_operation.insert_operation(deploy_id,"AutoHdmapMultiLaneAll",username,start_time,end_time,time_consuming,"还没方法取到状态")
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)

class AutohdmapMultilaneCheckVersion(base_http.BaseHandler):
    def process(self):
        try:
            app_name = self.get_arg('app_name')
            version = self.get_arg('version')
        except Exception as e:
            import traceback
            logger().error('bad args, query`[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        deploy_id = multilane_version_check.start()
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)
        return

class AutohdmapCheckVersion(base_http.BaseHandler):
    def process(self):
        try:
            app_name = self.get_arg('app_name')
            version = self.get_arg('version')
        except Exception as e:
            import traceback
            logger().error('bad args, query`[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        deploy_id = start_check_automap_version.start(app_name, version)
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)
        return

class TaskImgCheck(base_http.BaseHandler):
    def process(self):
        try:
            task_id = self.get_arg('task_id')
        except Exception as e:
            import traceback
            logger().error('bad args, query`[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        deploy_id = check_005_09.start(task_id)
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)
        return

class HistoryOperationHandler(base_http.BaseHandler):
    def process(self):
        data = history_operation.get_all_operation()
        mgr = template.ManagerV2(open('template/tables.html').read())
        for i in range(len(data)-1,-1,-1):
            d = data[i]
            res = {}
            res['deploy_id']= str(d['task_id'])
            res['task_name'] = str(d['task_name'])
            res['task_practitioners'] = str(d['task_practitioners'])
            res['start_time'] = str(d['task_start_time'])
            res['end_time'] = str(d['task_end_time'])
            res['time_consuming'] = str(d['time_consuming'])
            res['task_status'] = str(d['task_status'])
            print res
            mgr.add_ex('row', res)
        html = mgr.dump()
        self.write(html)
        #open('html/table_test.html', "w").write(html)

class TaskInfoHandler(base_http.BaseHandler):
    def process(self):
        mgr = template.ManagerV2(open('template/taskinfo.html').read())
        data = open('/opt/doraemon/liuhao_logs/task_info.txt', 'r').readlines()
        data.reverse()
        for line in data:
            print line.strip()
            res = json.loads(line.strip())
            mgr.add_ex('row', res)
        html = mgr.dump()
        self.write(html)

class ServiceJaguarV2Handler(base_http.BaseHandler):
    def get_info_from_hbase(self, project_id):
        url = 'http://10.11.5.248:9527/prd/general/kv/get' 
           
        namespace = 'jaguar_v2_status_statistics'
        payload = {}
        key = '%s_%s' % (namespace, project_id)
        payload["key"] = key 
        #logger().info('post key [%s] value [%s]', key, value)
        res = requests.get(url, data=payload)
        if res.status_code != 200:
            logger().error("return code is not 200")
            return False
        try:
            jdata = res.json()['result']
            logger().info('key [%s] resp [%s]', key, str(jdata))
            return jdata
        except Exception, e:
            import traceback
            traceback.print_exc(e)
            return False

    def process(self):
        project_id = self.get_arg('project_id')
        if not project_id:
            mgr = template.ManagerV2(open('html/jaguar_v2_search.html').read())
            html = mgr.dump()
            self.write(html)
        else:
            mgr = template.ManagerV2(open('html/jaguar_v2_proj_status.html').read())
            jdata = self.get_info_from_hbase(project_id)
            jdata = json.loads(jdata)
            jdata['project_id'] = project_id
            logger().info('%s %s %s' % (type(jdata), type(project_id), project_id))
            self.write(jdata)
            return
            mgr.add_ex('proj_info', jdata)
            html = mgr.dump()
            self.write(html)

class MultilaneClean(base_http.BaseHandler):
    def process(self):
        name = self.get_arg('multilane')
        username = user.match_name(self.get_arg('username'))
        start_time = time.time()
        if name == "start":
            deploy_id = zhang_clean_mtask.start()
        elif name == "stop":
            deploy_id = zhang_clean_mtask.stop()
        elif name == "restart":
            deploy_id = zhang_clean_mtask.restart()
        elif name == "clean":
            deploy_id = zhang_clean_mtask.clean()
        elif name == "version":
            deploy_id = zhang_clean_mtask.version()
        end_time = time.time()
        time_consuming = end_time - start_time
        start_time = timer.format_time(start_time)
        end_time = timer.format_time(end_time)
        history_operation.insert_operation(deploy_id,"Multilane_"+name, username,start_time,end_time,time_consuming,"还没有想到怎么获取状态的值")
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)

class LaneClean(base_http.BaseHandler):
    def process(self):
        name = self.get_arg('lane')
        username = user.match_name(self.get_arg('username'))
        start_time = time.time()
        if name == "start":
            deploy_id = zhang_clean_ltask.start()
        elif name == "stop":
            deploy_id = zhang_clean_ltask.stop()
        elif name == "restart":
            deploy_id = zhang_clean_ltask.restart()
        elif name == "clean":
            deploy_id = zhang_clean_ltask.clean()
        elif name == "version":
            deploy_id = zhang_clean_ltask.version()
        end_time = time.time()
        time_consuming = end_time - start_time
        start_time = timer.format_time(start_time)
        end_time = timer.format_time(end_time)
        history_operation.insert_operation(deploy_id,"Lane_"+name, username,start_time,end_time,time_consuming,"还没有想到怎么获取状态的值")
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)

class ZabbixBIHandler(base_http.BaseHandler):
    def process(self):
        mgr = template.ManagerV2(open('template/zabbixbi.html').read())
        data = open('/opt/doraemon/zabbixbi/hadoopinfo.txt', 'r').readlines()
        for line in data:
            print line.strip()
            res = json.loads(line.strip())
            print res
            mgr.add_ex('row', res)
        html = mgr.dump()
        self.write(html)


class ApiAutohdmapHandler(base_http.BaseHandler):
    def process(self):
        action = self.get_arg('action') 
        if action == "start":
            msg = autohdmap_api.dostart()
        elif action == "stop":
            msg = autohdmap_api.dostop()
        elif action == "restart":
            msg = autohdmap_api.dorestart()

        if msg:
            self.set_json_result(make_success_result_int('Success to restart'))
        else:
            self.set_json_result(make_error_result(1, 'Failed to restart'))
	return

class ApiMultilaneHandler(base_http.BaseHandler):
    def process(self):
        action = self.get_arg('action') 
        if action == "start":
            msg = multilane_api.dostart()
        elif action == "stop":
            msg = multilane_api.dostop()
        elif action == "restart":
            msg = multilane_api.dorestart()

        if msg:
            self.set_json_result(make_success_result_int('Success to restart'))
        else:
            self.set_json_result(make_error_result(1, 'Failed to restart'))
	return

class ProblemHandler(base_http.BaseHandler):
    def process(self):
        data = insert_mongo.get_all_problem()
        mgr = template.ManagerV2(open('template/problem.html').read())
        for i in range(len(data)-1,-1,-1):
            d = data[i]
            res = {}
            res['title']= str(d['title'])
            res['message'] = str(d['message'])
            res['insert_time'] = str(d['insert_time'])
            res['status'] = str(d['status'])
            print res
            mgr.add_ex('row', res)
        html = mgr.dump()
        self.write(html)

class VersionHandler(base_http.BaseHandler):
    def process(self):
        collection_name = self.get_arg('collection_name')
	username = user.match_name(self.get_arg('username'))
	version_control.get_all_version(collection_name)

class VersionShowHandler(base_http.BaseHandler):
    def process(self):
        data = version_control.get_all_version()
        mgr = template.ManagerV2(open('template/version_show.html').read())
        print data
        for i in range(len(data)-1,-1,-1):
            d = data[i]
            res = {}
            res['service_name']= str(d['service_name'])
            res['service_version'] = str(d['service_version'])
            res['insert_time'] = str(d['insert_time'])
            print res
            mgr.add_ex('row', res)
        html = mgr.dump()
        self.write(html)

class ModelReleaseHandler(base_http.BaseHandler):
    def process(self):
        try:
            model_name = self.get_arg('model_name')
        except Exception as e:
            import traceback
            logger().error('bad args, query`[%s]', self.request.query)
            self.set_json_result(make_error_result(2, str(e)))
            return
        deploy_id = model_release.start(model_name)
        self.redirect('/api/deploy/status?deployId=%s' % deploy_id)
        return

class InfoCsvHandler(base_http.BaseHandler):
    def process(self):
        tag = info_csv.dostart()
	if tag == True:
		self.write("info.csv success     Visit http://10.11.5.121:9527/model/list?adcode=110000  authenticating")
	elif tag == False:
		self.write("info.csv failed")
        #self.redirect('/api/deploy/status?deployId=%s' % deploy_id)
        return

class VersionManagementGetHandler(base_http.BaseHandler):
    def process(self):
        try:
            service_name = self.get_arg('service_name')
        except Exception as e:
            self.set_json_result(make_error_result(2, str(e)))
            return
        ret = version_management.get(service_name)
        logger().info('get service[%s] version[%s]', service_name, ret)
        res = make_success_result(ret)
        self.set_json_result(res)

class VersionManagementGetAllHandler(base_http.BaseHandler):
    def process(self):
        try:
            pass
        except Exception as e:
            self.set_json_result(make_error_result(2, str(e)))
            return
        ret = version_management.get_all()
        for service_name, version in ret.items():
            logger().info('service_name[%s], version[%s]',
                          service_name, version)
        self.set_header('Access-Control-Allow-Origin', '*')
        res = make_success_result(ret)
        self.set_json_result(res)

class VersionManagementSetHandler(base_http.BaseHandler):
    def process(self):
        try:
            service_name = self.get_arg('service_name')
            service_version = self.get_arg('service_version')
        except Exception as e:
            self.set_json_result(make_error_result(2, str(e)))
            return
        logger().info('set Version Management [%s],[%s]', service_name, service_version)
        ret = version_management.set(service_name, service_version)
        if not ret:
            logger().error('insert mongo failed')
            res = make_error_result('-1', 'insert mongo failed')
        else:
            res = make_success_result(ret)
        self.set_json_result(res)

class BJTestVersionManagementGetHandler(base_http.BaseHandler):
    def process(self):
        try:
            service_name = self.get_arg('service_name')
        except Exception as e:
            self.set_json_result(make_error_result(2, str(e)))
            return
        ret = bj_test_version_management.get(service_name)
        logger().info('get service[%s] version[%s]', service_name, ret)
        res = make_success_result(ret)
        self.set_json_result(res)

class BJTestVersionManagementGetAllHandler(base_http.BaseHandler):
    def process(self):
        try:
            pass
        except Exception as e:
            self.set_json_result(make_error_result(2, str(e)))
            return
        ret = bj_test_version_management.get_all()
        for service_name, version in ret.items():
            logger().info('service_name[%s], version[%s]',
                          service_name, version)
        self.set_header('Access-Control-Allow-Origin', '*')
        res = make_success_result(ret)
        self.set_json_result(res)

class BJTestVersionManagementSetHandler(base_http.BaseHandler):
    def process(self):
        try:
            service_name = self.get_arg('service_name')
            service_version = self.get_arg('service_version')
        except Exception as e:
            self.set_json_result(make_error_result(2, str(e)))
            return
        logger().info('set Version Management [%s],[%s]', service_name, service_version)
        ret = bj_test_version_management.set(service_name, service_version)
        if not ret:
            logger().error('insert mongo failed')
            res = make_error_result('-1', 'insert mongo failed')
        else:
            res = make_success_result(ret)
        self.set_json_result(res)

class BJTestVersionManagementDefaultSetHandler(base_http.BaseHandler):
    def process(self):
        try:
            stage = self.get_arg('stage')
            default_version = self.get_arg('default_version')
        except Exception as e:
            self.set_json_result(make_error_result(2, str(e)))
            return
        logger().info('set Version Management [%s],[%s]', stage, default_version)
        ret = bj_test_version_management.default_set(stage, default_version)
        if not ret:
            logger().error('insert mongo failed')
            res = make_error_result('-1', 'insert mongo failed')
        else:
            res = make_success_result(ret)
        self.set_json_result(res)

app = tornado.web.Application(
    [
        (r"/test", TestHandler),
 	(r"/zabbixbi.html", ZabbixBIHandler),
        (r"/api/reco/deploy/start", RecoDeployStartHandler),
        (r"/api/lane_clean/deploy/start", LaneClean),
        (r"/api/multilane_clean/deploy/start", MultilaneClean),
        (r"/api/deploy/status", DeployStatusHandler),
        (r"/api/autohdmap_lane/deploy/start", AutoHdmapLaneDeployStartHandler),
        (r"/api/poc/deploy/start", JavaServiceDeployStartHandler),
        (r"/api/autohdmap_fusion/deploy/start", AutoHdmapFusionDeployStartHandler),
        (r"/api/autohdmap_multilane/deploy/start", AutoHdmapMultiLaneDeployStartHandler),
        (r"/api/hbase-store/deploy/start", HbaseStoreStartHandler),
        (r"/api/mesh_release/deploy/start", MeshReleaseStartHandler),
	(r"/api/hadoop_transfile/deploy/start", HadoopTransFileStartHandler),
        (r"/api/web_release/deploy/start", WebReleaseStartHandler),
        (r"/api/mesh_restart/deploy/start", MeshRestartStartHandler),
        (r"/api/mesh_hbase_imagequery/deploy/start", MeshHbaseImageStartHandler),
        (r"/api/autohdmap_lane_clean_up/deploy/start", AutohdmaplaneCleanUPStartHandler),
        (r"/api/imagequery/deploy/start", ImageStartHandler),
        (r"/api/auto/info", AutoInfoHandler),
        (r"/api/login", LoginHandler),
        (r"/api/logout", LogoutHandler),
        (r"/api/msg/send", SendMsgHandler),
        (r"/api/msg/send/text", SendMsgTextHandler),
        (r"/api/autohdmap/action", ApiAutohdmapHandler),
        (r"/api/multilane/action", ApiMultilaneHandler),
        (r"/api/autohdmap_lane_one/control", AutoHdmapLaneOneControlHandler),
        (r"/api/autohdmap_lane_all/control", AutoHdmapLaneAllControlHandler),
        (r"/api/java_release/deploy/start", JavareleaseStartHandler),
        (r"/api/autohdmap_multilane_one/control", AutoHdmapMultiLaneOneControlHandler),
        (r"/api/autohdmap_multilane_all/control", AutoHdmapMultiLaneAllControlHandler),
        (r"/api/autohdmap_lane/version/check", AutohdmapCheckVersion),
        (r"/api/autohdmap_multilane/version/check", AutohdmapMultilaneCheckVersion),
        (r"/api/task_img/check", TaskImgCheck),
        (r"/api/model/release", ModelReleaseHandler),
        (r"/dashboard.html", DashboardHandler),
	(r"/tables.html", HistoryOperationHandler),
	(r"/problem.html", ProblemHandler),
	(r"/api/version_insert/deploy/start", VersionHandler),
	(r"/version_show.html", VersionShowHandler),
        (r"/", WelcomeHandler),
 	(r"/taskinfo.html", TaskInfoHandler),
 	(r"/api/service_jaguar_v2", ServiceJaguarV2Handler),
        (r"/api/model/info_csv", InfoCsvHandler),

        (r"/api/service_version/get", VersionManagementGetHandler),
        (r"/api/service_version/get_all", VersionManagementGetAllHandler),
        (r"/api/service_version/set", VersionManagementSetHandler),

        (r"/api/bj_test_service_version/get", BJTestVersionManagementGetHandler),
        (r"/api/bj_test_service_version/get_all", BJTestVersionManagementGetAllHandler),
        (r"/api/bj_test_service_version/set", BJTestVersionManagementSetHandler),
        (r"/api/bj_test_service_version/set_default", BJTestVersionManagementDefaultSetHandler),
    ],cookie_secret='7ef05292-a289-40d5-9ff7-80510c323c8b'
)


def main():
    log_init('info', 'logs/service.txt', quiet=False)
    sockets = tornado.netutil.bind_sockets(int(opt.option().port))
    tornado.process.fork_processes(5)
    server = tornado.httpserver.HTTPServer(app)
    server.add_sockets(sockets)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
