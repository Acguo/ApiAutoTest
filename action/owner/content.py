# coding:utf-8
import requests
import json

from utils import utils
from utils.pylog import Pylog
from auth.authors import Authors
from config import globalvars


class Content:
    '''内容管理'''

    def __init__(self, auth=None):
        self.config = globalvars.config()
        self.api = self.config.api
        owner = self.config.owner
        self.host = owner["env"]["host_mb"]
        self.headers = globalvars.get_value("headers_owner")
        self.headers["Origin"] = owner["env"]["origin_yz"]

    def site_view(self):
        '''站点信息'''
        url = "http://" + self.host + self.api["owner"]["site_view"]
        resp = requests.get(url=url, headers=self.headers)
        Pylog.debug("【站点信息-resp】" + str(resp.text))
        #保存站点信息cid
        globalvars.set_value("site_cid", json.loads(resp.text)["data"]['cid'])
        return str(resp.text)

    def site_save(self, param):
        '''保存站点信息'''
        url = "http://" + self.host + self.api["owner"]["site_save"]
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(param), timeout=15)
        Pylog.debug("【保存站点信息-request】" + str(param))
        Pylog.debug("【保存站点信息-resp】" + str(resp.text))
        return str(resp.text)

    def copyright_list(self, type=1):
        '''网站说明文案'''
        url = "http://" + self.host + self.api["owner"]["copyright_list"]
        datas = {"type": type}
        resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
        if type == 1:
            Pylog.debug("【首页文案信息-resp】" + str(resp.text))
        elif type == 2:
            Pylog.debug("【注册说明信息-resp】" + str(resp.text))
        elif type == 3:
            Pylog.debug("【线上存取文案信息-resp】" + str(resp.text))
        elif type == 4:
            Pylog.debug("【帮助中心信息-resp】" + str(resp.text))

        return str(resp.text)

    def copyright_save(self, param):
        '''修改网站说明文案'''
        url = "http://" + self.host + self.api["owner"]["copyright_save"]
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(param), timeout=15)
        Pylog.debug("【修改网站说明文案-resp】" + str(resp.text))
        return str(resp.text)

    def activity_list(self):
        '''搜索优惠活动列表'''
        try:
            url = "http://" + self.host + self.api["owner"]["activity_list"]
            datas = {"page": 1, "rows": 15}
            resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
            Pylog.debug("【搜索优惠活动列表-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【搜索优惠活动列表错误】：" + Pylog.exinfo())
            return "搜索优惠活动列表错误"

    def activity_save(self, param):
        '''修改优惠活动'''
        try:
            url = "http://" + self.host + self.api["owner"]["activity_save"]
            datas = json.loads(self.activity_list())["data"]["rows"][0]
            datas["content"] = "<p>{}</p>".format(param)
            Pylog.debug("【修改优惠活动-request】" + str(param))
            resp = requests.post(url=url, headers=self.headers, data=json.dumps(datas), timeout=15)
            Pylog.debug("【修改优惠活动-resp】" + str(resp.text))
            globalvars.set_value("activity_cid", json.loads(resp.text)["data"])
            return resp.text
        except Exception:
            Pylog.error("【修改优惠活动错误】：" + Pylog.exinfo())
            return "修改优惠活动错误"

    def activity_create(self, param = {"title":"123","weight":"1","titlePic":"T16tbTByJT1RCvBVKd","content":"<p>123123</p>","beginTime":1523894400000,"endTime":1523980799000}):
        '''新建并启用优惠活动'''
        url = "http://" + self.host + self.config.api["owner"]["activity_save"]
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(param), timeout=15)
        globalvars.set_value("actCid", json.loads(resp.text)["data"])
        Pylog.debug("【新建优惠活动-request】" + str(param))
        Pylog.debug("【新建优惠活动-resp】" + str(resp.text))
        return str(resp.text)

    def carousel_list(self):
        '''搜索轮播图列表'''
        url = "http://" + self.host + self.api["owner"]["carousel_list"]
        datas = {"page": 1, "rows": 15}
        Pylog.debug("【搜索轮播图列表-request】" + str(datas))
        resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【搜索轮播图列表-resp】" + str(resp.text))
        return resp.text

    def carousel_save(self, link):
        '''修改轮播图'''
        try:
            url = "http://" + self.host + self.api["owner"]["carousel_save"]
            url_view = "http://" + self.host + "/ares-cms/apis/plat/carousel/view"
            url_save = "http://" + self.host + "/ares-cms/apis/plat/carousel/save"
            cid = json.loads(self.carousel_list())["data"]["rows"][0]["cid"]
            viewdata = requests.get(url=url_view, headers=self.headers, params={"id": cid}, timeout=15)
            Pylog.debug("【view轮播图-resp】" + str(viewdata.text))
            viewdata = json.loads(viewdata.text)["data"]
            viewdata["itemPO"][0]["link"] = link
            Pylog.debug("【修改轮播图-request】" + str(viewdata))
            resp = requests.post(url=url_save, headers=self.headers, data=json.dumps(viewdata), timeout=15)
            Pylog.debug("【修改轮播图-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【修改轮播图错误】：" + Pylog.exinfo())
            return "修改轮播图错误"

    def notice_list(self, title=None, status=0):
        '''搜索公告列表'''
        url = "http://" + self.host + self.api["owner"]["notice_list"]
        datas = {"page": 1, "rows": 15, "status": status, "title": title}
        resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【搜索公告列表-request】" + str(datas))
        Pylog.debug("【搜索公告列表-resp】" + str(resp.text))
        return str(resp.text)

    def notice_create(self, datas):
        '''创建并启用公告'''
        try:
            bodys = {}
            url = "http://" + self.host + "/ares-cms/apis/plat/notice/save"
            datas = {"title": "自动化测试公告", "content": datas, "weight": 99}
            resp = requests.post(url=url, headers=self.headers,
                                 data=json.dumps(datas), timeout=15)
            # 保存入参
            globalvars.set_value("noticeTitle", datas['title'])
            globalvars.set_value("noticeWeight", datas['weight'])
            globalvars.set_value("noticeContent", datas['content'])

            Pylog.debug("【创建公告-resp】" + resp.text)
            for i in json.loads(self.notice_list())["data"]["rows"]:
                if str(i["cid"]) == str(json.loads(resp.text)["data"]):
                    bodys = i
            bodys["status"] = 1
            Pylog.debug("【启用公告-request】" + str(bodys))
            resp = requests.post(url=url, headers=self.headers, data=json.dumps(bodys), timeout=15)
            Pylog.debug("【启用公告-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error("【创建并启用公告错误】：" + Pylog.exinfo())
            return "创建并启用公告错误"

    def notice_save(self, param):
        '''修改公告'''
        url = "http://" + self.host + self.api["owner"]["notice_save"]
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(param), timeout=15)
        Pylog.debug("【修改公告-request】" + str(param))
        Pylog.debug("【修改公告-resp】" + str(resp.text))
        return str(resp.text)

    def popText_list(self):
        '''搜索首页弹屏列表'''
        url = "http://" + self.host + self.api["owner"]["popText_list"]
        datas = {"page": 1, "rows": 15}
        resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【搜索首页弹屏列表-request】" + str(datas))
        Pylog.debug("【搜索首页弹屏列表-resp】" + str(resp.text))
        return str(resp.text)

    def popText_create(self, datas):
        '''创建并启用首页弹屏'''
        try:
            url = "http://" + self.host + "/ares-cms/apis/plat/popText/save"
            datas = {"title": "自动化测试弹屏", "content": datas}
            Pylog.debug("【创建首页弹屏-requsts】" + str(datas))
            resp = requests.post(url=url, data=json.dumps(datas), headers=self.headers, timeout=15)
            # 保存入参
            globalvars.set_value("popTextTitle", datas['title'])
            globalvars.set_value("popTextContent", datas['content'])

            Pylog.debug("【创建首页弹屏-resp】" + str(resp.text))
            bodys = {}
            for i in json.loads(self.popText_list())["data"]["rows"]:
                if str(json.loads(resp.text)["data"]) == str(i["cid"]):
                    bodys = i
            bodys["status"] = 1
            Pylog.debug("【启用首页弹屏-requsts】" + str(bodys))
            resp = requests.post(url=url, data=json.dumps(bodys), headers=self.headers, timeout=15)
            Pylog.debug("【启用首页弹屏-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【创建并启用首页弹屏错误】：" + Pylog.exinfo())
            return "创建并启用首页弹屏错误"

    def popText_save(self, param):
        '''修改首页弹屏'''
        url = "http://" + self.host + self.auth.config.api["owner"]["popText_save"]
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(param), timeout=15)
        Pylog.debug("【修改首页弹屏-request】" + str(param))
        Pylog.debug("【修改首页弹屏-resp】" + str(resp.text))
        return str(resp.text)

    def msgTemplate_list(self, title=None, status=0):
        '''搜索信息模板列表'''
        url = "http://" + self.host + self.auth.config.api["owner"]["msgTemplate_list"]
        datas = {"page": 1, "rows": 15, "status": status, "title": title}
        resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【搜索信息模板列表-request】" + str(datas))
        Pylog.debug("【搜索信息模板列表-resp】" + str(resp.text))
        return str(resp.text)

    def msgTemplate_save(self, param):
        '''修改信息模板'''
        url = "http://" + self.host + self.auth.config.api["owner"]["msgTemplate_save"]
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(param), timeout=15)
        Pylog.debug("【修改信息模板-request】" + str(param))
        Pylog.debug("【修改信息模板-resp】" + str(resp.text))
        return str(resp.text)

    def instationMsg_list(self, title=None, modifyTimeEnd=1519833599000, modifyTimeStart=1517414400000):
        '''搜索站内信列表'''
        url = "http://" + self.host + self.auth.config.api["owner"]["instationMsg_list"]
        datas = {"page": 1, "rows": 15, "modifyTimeEnd": modifyTimeEnd, "modifyTimeStart": modifyTimeStart,
                 "title": title}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【搜索站内信列表-request】" + str(datas))
        Pylog.debug("【搜索站内信列表-resp】" + str(resp.text))
        return str(resp.text)

    def instationMsg_save(self, content="测试数据test data！！"):
        '''发送站内信'''
        try:
            url = "http://" + self.host + self.api["owner"]["instationMsg_save"]
            param = {"title": "autotest", "content": content, "receiveType": 0, "receiveBody": "", "supportTerminal": 3}
            Pylog.debug("【发送站内信-request】" + str(param))
            resp = requests.post(url=url, headers=self.headers, data=json.dumps(param), timeout=15)
            Pylog.debug("【发送站内信-resp】" + str(resp.text))
            globalvars.set_value("instationMsg", content)
            globalvars.set_value("msgContent", content)
            globalvars.set_value("msgTitle", param['title'])
            return resp.text
        except Exception:
            Pylog.error("【发送站内信】：" + Pylog.exinfo())
            return "发送站内信错误"

    def bulletin_list(self, title=None, endTime=1519833599000, startTime=1517414400000):
        '''搜索公告通知'''
        url = "http://" + self.host + self.api["owner"]["bulletin_list"]
        datas = {"page": 1, "rows": 15, "endTime": endTime, "startTime": startTime, "title": title, "bulletinType": 1,
                 "sideType": 2}
        resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【搜索公告通知-request】" + str(datas))
        Pylog.debug("【搜索公告通知-resp】" + str(resp.text))
        return str(resp.text)

    def activity_delete(self, ids):
        '''优惠活动删除'''
        try:
            url = "http://" + self.host + "/ares-cms/apis/plat/activity/save"
            url_d = "http://" + self.host + self.api["owner"]["activity_delete"]
            datas = json.loads(self.activity_list())["data"]["rows"][0]
            # globalvars.set_value("actParam", datas)
            datas["cid"] = ids
            datas["status"] = 0
            resp = requests.post(url=url, headers=self.headers, data=json.dumps(datas), timeout=15)
            Pylog.debug("【优惠活动停用-resp】" + str(resp.text))

            resp = requests.get(url=url_d, headers=self.headers, params={"cid": ids}, timeout=15)
            Pylog.debug("【优惠活动删除-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【优惠活动删除错误】：" + Pylog.exinfo())
            return "优惠活动删除错误"

    def activity_deleteAll(self):
        '''优惠活动删除全部'''
        try:
            clist = self.activity_list()
            clist = json.loads(clist)["data"]["rows"]
            for i in clist:
                self.activity_delete(i["cid"])
            return "SUCCESS"
        except Exception:
            Pylog.error("【优惠活动删除全部错误】：" + Pylog.exinfo())
            return "优惠活动删除全部错误"

    def carousel_delete(self, ids):
        '''轮播图删除'''
        try:
            url = "http://" + self.host + "/ares-cms/apis/plat/carousel/save"
            url_d = "http://" + self.host + self.api["owner"]["carousel_delete"]
            datas = json.loads(self.carousel_list())["data"]["rows"][0]
            id = datas["cid"]
            #停用轮播图
            datas["cid"] = ids
            datas["status"] = 0
            resp = requests.post(url=url, headers=self.headers, data=json.dumps(datas), timeout=15)
            Pylog.debug("【轮播图停用-resp】" + str(resp.text))

            resp = requests.get(url=url_d, headers=self.headers, params={"cid": ids}, timeout=15)
            Pylog.debug("【轮播图删除-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【轮播图删除错误】：" + Pylog.exinfo())
            return "轮播图删除错误"

    def carousel_deleteAll(self):
        '''轮播图删除全部'''
        try:
            clist = self.carousel_list()
            clist = json.loads(clist)["data"]["rows"]
            for i in clist:
                self.carousel_delete(i["cid"])
            return "SUCCESS"
        except Exception:
            Pylog.error("【轮播图删除全部错误】：" + Pylog.exinfo())
            return "轮播图删除全部错误"

    def carousel_create(self, param = {"beginTime":1523894400000,"delayTime":"1","endTime":1523980799000,"itemPO":[{"link":"http://www.baidu.com","titlePic":"T1wRWTByJT1RCvBVdK"},{"link":"","titlePic":""}],"title":"123"}):
        '''新建并启用轮播图'''
        url = "http://" + self.host + self.config.api["owner"]["carousel_save"]
        url_view = "http://" + self.host + "/ares-cms/apis/plat/carousel/view"
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(param), timeout=15)
        globalvars.set_value("carouselCid", json.loads(resp.text)["data"])
        Pylog.debug("【新建轮播图-request】" + str(param))
        Pylog.debug("【新建轮播图-resp】" + str(resp.text))
        # 查询轮播图信息
        viewdata = requests.get(url=url_view, headers=self.headers, params={"id": json.loads(resp.text)["data"]},
                                timeout=15)
        viewdata = json.loads(viewdata.text)["data"]
        viewdata['status'] = 1
        # 启用轮播图
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(viewdata), timeout=15)
        Pylog.debug("【启用轮播图-request】" + str(viewdata))
        Pylog.debug("【启用轮播图-resp】" + str(resp.text))
        return str(resp.text)

    def notice_delete(self, ids):
        '''公告删除'''
        try:
            url_save = "http://" + self.host + self.api["owner"]["notice_save"]
            url_d = "http://" + self.host + self.api["owner"]["notice_delete"]
            datas = json.loads(self.notice_list(status=None))["data"]["rows"][0]
            datas["cid"] = ids
            datas["status"] = 0
            resp = requests.post(url=url_save, headers=self.headers, data=json.dumps(datas), timeout=15)
            Pylog.debug("【公告停用-resp】" + str(resp.text))

            resp = requests.get(url=url_d, headers=self.headers, params={"cid": ids}, timeout=15)
            Pylog.debug("【公告删除-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【公告删除错误】：" + Pylog.exinfo())
            return "公告删除错误"

    def notice_deleteAll(self):
        '''公告删除全部'''
        try:
            clist = self.notice_list(status=None)
            clist = json.loads(clist)["data"]["rows"]
            for i in clist:
                self.notice_delete(i["cid"])
            return "SUCCESS"
        except Exception:
            Pylog.error("【公告删除全部错误】：" + Pylog.exinfo())
            return "公告删除全部错误"

    def popText_delete(self, ids):
        '''首页弹屏删除'''
        try:
            url_save = "http://" + self.host + self.api["owner"]["popText_save"]
            url_d = "http://" + self.host + self.api["owner"]["popText_delete"]
            datas = json.loads(self.popText_list())["data"]["rows"][0]
            datas["cid"] = ids
            datas["status"] = 0
            resp = requests.post(url=url_save, headers=self.headers, data=json.dumps(datas), timeout=15)
            Pylog.debug("【首页弹屏停用-resp】" + str(resp.text))

            resp = requests.get(url=url_d, headers=self.headers, params={"cid": ids}, timeout=15)
            Pylog.debug("【首页弹屏删除-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【首页弹屏删除错误】：" + Pylog.exinfo())
            return "首页弹屏删除错误"

    def popText_deleteAll(self):
        '''首页弹屏删除全部'''
        try:
            clist = self.popText_list()
            clist = json.loads(clist)["data"]["rows"]
            for i in clist:
                self.popText_delete(i["cid"])
            return "SUCCESS"
        except Exception:
            Pylog.error("【首页弹屏删除全部错误】：" + Pylog.exinfo())
            return "首页弹屏删除全部错误"

    def carousel_view(self,cid):
        '''轮播图信息'''
        url = "http://" + self.host + self.api["owner"]["carousel_view"]
        resp = requests.get(url=url, headers=self.headers, params={"id": cid})
        Pylog.debug("【轮播图信息-resp】" + str(resp.text))
        return str(resp.text)

    def upLoadFile(self, fileName):
        '''上传文件'''
        try:
            paths = utils.findPath()
            url_up = "http://admin.baochiapi.com/photo/upload"
            file_up = {'pic': (open(paths + 'datas\\{}'.format(str(fileName)), 'rb'), 'image/png')}
            self.headers["Content-Type"] = None
            self.headers["Accept"] = "*/*"
            picid = requests.post(url=url_up, files=file_up, headers=self.headers)
            picid = json.loads(picid.text)["picid"]

            return picid
        except Exception:
            Pylog.error("【上传文件错误】：" + Pylog.exinfo())
            return "上传文件错误"


if __name__ == "__main__":
    Pylog()
    globalvars._init()
    Authors()
    Content().activity_save("哈哈哈哈")
