# coding:utf-8
import requests
import time

from utils import utils
from auth.authors import Authors
from utils.pylog import Pylog
from config import globalvars

class Statistics():
    '''运营分析'''
    def __init__(self, auth=None):
        self.config = globalvars.config()
        self.api = self.config.api
        owner = self.config.owner
        self.host = owner["env"]["host_yz"]
        self.headers = globalvars.get_value("headers_owner")
        self.headers["Origin"] = owner["env"]["origin_yz"]

    def statistics_inout(self, memberName, startTime, endTime):
        '''出入款统计搜索'''
        try:
            startTime = utils.datetime_timestamp(startTime) * 1000
            endTime = utils.datetime_timestamp(endTime) * 1000
            url = "http://" + self.host + self.config.api["owner"]["statistics_inout"]
            datas = {"memberName": memberName, "endTime": endTime, "page": 1, "rows": 15, "startTime": startTime}
            resp = requests.get(url=url, headers=self.headers, params=datas)
            Pylog.debug("【出入款统计搜索-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error("【出入款统计搜索错误】：" + Pylog.exinfo())
            return "出入款统计搜索错误"

    def statistics_inList(self, endTime=1519833599000, startTime=1517414400000, memberName=None):
        '''会员入款明细'''
        url = "http://" + self.host + self.auth.config.api["owner"]["statistics_inList"]
        datas = {"endTime": endTime, "page": 1, "rows": 15, "startTime": startTime, "memberName": memberName}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【会员入款明细-request】" + str(datas))
        Pylog.info("【会员入款明细-resp】" + str(resp.text))
        return str(resp.text)

    def statistics_outList(self, endTime=1519833599000, startTime=1517414400000, memberName=None):
        '''会员出款明细'''
        url = "http://" + self.host + self.auth.config.api["owner"]["statistics_outList"]
        datas = {"endTime": endTime, "page": 1, "rows": 15, "startTime": startTime, "memberName": memberName}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【会员出款明细-request】" + str(datas))
        Pylog.info("【会员出款明细-resp】" + str(resp.text))
        return str(resp.text)

    def discount_agent(self, endTime=1519833599000, startTime=1517414400000):
        '''搜索会员优惠统计'''
        url = "http://" + self.host + self.auth.config.api["owner"]["discount_agent"]
        datas = {"endTime": endTime, "page": 1, "rows": 15, "startTime": startTime}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【搜索会员优惠统计-request】" + str(datas))
        Pylog.info("【搜索会员优惠统计-resp】" + str(resp.text))
        return str(resp.text)

    def discount_member(self, endTime=1519833599000, startTime=1517414400000, agentName='default'):
        '''查看会员优惠列表'''
        url = "http://" + self.host + self.auth.config.api["owner"]["discount_member"]
        datas = {"endTime": endTime, "page": 1, "rows": 15, "startTime": startTime, "agentName": agentName}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【查看会员优惠列表-request】" + str(datas))
        Pylog.info("【查看会员优惠列表-resp】" + str(resp.text))
        return str(resp.text)

    def member_list(self, endTime=1519833599000, startTime=1517414400000, actionType=13, memberName='adamwf01'):
        '''查看会员优惠详情
            actionType:
                13：活动优惠
        '''
        url = "http://" + self.host + self.auth.config.api["owner"]["member_list"]
        datas = {"endTime": endTime, "page": 1, "rows": 15, "startTime": startTime, "actionType": actionType, "memberName": memberName}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【查看会员优惠详情-request】" + str(datas))
        Pylog.info("【查看会员优惠详情-resp】" + str(resp.text))
        return str(resp.text)

    def mem_cash_back_record(self, endTime=1519833599000, startTime=1517414400000, type=1):
        '''查看会员返水记录
            type:
                1：会员
        '''
        url = "http://" + self.host + self.auth.config.api["owner"]["mem_cash_back_record"]
        datas = {"endTime": endTime, "page": 1, "rows": 15, "startTime": startTime, "type": type}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【查看会员返水记录-request】" + str(datas))
        Pylog.info("【查看会员返水记录-resp】" + str(resp.text))
        return str(resp.text)

    def order_withhold(self, endTime=1519833599000, startTime=1517414400000):
        '''查看会员扣款记录'''
        url = "http://" + self.host + self.auth.config.api["owner"]["order_withhold"]
        datas = {"endTime": endTime, "page": 1, "rows": 15, "startTime": startTime}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【查看会员扣款记录-request】" + str(datas))
        Pylog.info("【查看会员扣款记录-resp】" + str(resp.text))
        return str(resp.text)

    def levelStatistics_list(self, endTime=1519833599000, startTime=1517414400000):
        '''查看会员分层统计'''
        url = "http://" + self.host + self.auth.config.api["owner"]["levelStatistics_list"]
        datas = {"endTime": endTime, "page": 1, "rows": 15, "startTime": startTime}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【查看会员分层统计-request】" + str(datas))
        Pylog.info("【查看会员分层统计-resp】" + str(resp.text))
        return str(resp.text)

    def levelStatistics_member_list(self, endTime=1519833599000, startTime=1517414400000, levelIds=410, lotteryIds=2):
        '''查看会员注单统计'''
        url = "http://" + self.host + self.auth.config.api["owner"]["levelStatistics_member_list"]
        datas = {"endTime": endTime, "page": 1, "rows": 15, "startTime": startTime, "levelIds": levelIds, "lotteryIds": lotteryIds}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【查看会员注单统计-request】" + str(datas))
        Pylog.info("【查看会员注单统计-resp】" + str(resp.text))
        return str(resp.text)

    def statistics_memberDaylist(self, startTime=1517414400000, endTime=1519833599000):
        '''搜索新增会员统计'''
        url = "http://" + self.host + self.auth.config.api["owner"]["statistics_memberDaylist"]
        datas = {"page": 1, "rows": 15, "endTime": endTime, "startTime": startTime}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.debug("【搜索新增会员统计-request】" + str(datas))
        Pylog.info("【搜索新增会员统计-resp】" + str(resp.text))
        return str(resp.text)

    def online_list(self, memberName=None):
        '''在线会员查询'''
        url = "http://" + self.host + self.auth.config.api["owner"]["online_list"]
        datas = {"page": 1, "rows": 15, "memberName": memberName}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.debug("【在线会员查询-request】" + str(datas))
        Pylog.info("【在线会员查询-resp】" + str(resp.text))
        return str(resp.text)

if __name__ == "__main__":
    Pylog()
    globalvars._init()
    Authors("owner")
    statistics = Statistics()
    starttime = time.strftime("%Y-%m-%d", time.gmtime()) + " 00:00:00"
    endtime = time.strftime("%Y-%m-%d", time.gmtime()) + " 23:59:59"
    statistics.statistics_inout("auto_pt2_17", starttime, endtime)
