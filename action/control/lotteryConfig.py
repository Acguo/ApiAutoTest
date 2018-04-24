# coding:utf-8
import requests
import json

from config import globalvars
from utils.pylog import Pylog
from auth.authors import Authors


class LotteryConfig():
    def __init__(self):
        self.config = globalvars.config()
        self.api = self.config.api
        owner = self.config.owner
        self.host = owner["env"]["host_ct"]
        self.headers = globalvars.get_value("headers_control")
        self.headers["Origin"] = owner["env"]["origin_ct"]
        self.platId = owner["env"]["platId"]

    def lottery_list(self):
        '''彩种管理列表'''
        url = "http://" + self.host + self.api["control"]["lottery_list"]
        resp = requests.get(url=url, headers=self.headers, timeout=15)
        Pylog.debug("【彩种管理列表-resp】" + str(resp.text))
        return resp.text

    def get_plat2odds(self):
        '''获取平台商与赔率绑定关系'''
        try:
            url = "http://" + self.host + "/areaaccount/apis/platinfo/get"
            resp = requests.get(url=url, headers=self.headers, params={"platInfoId": self.platId}, timeout=15)
            Pylog.debug("【获取平台商与赔率绑定关系-resp】" + str(resp.status_code))
            return resp.text
        except Exception:
            Pylog.error("【获取平台商与赔率绑定关系错误】：" + Pylog.exinfo())
            return "获取平台商与赔率绑定关系错误"

    def odds_get(self, oddsId):
        '''获取赔率详情'''
        try:
            url = "http://" + self.host + "/ares-config/apis/odds/view"
            resp = requests.get(url=url, headers=self.headers, params={"id": oddsId}, timeout=15)
            Pylog.debug("【获取赔率详情-resp】" + str(resp.status_code))
            return resp.text
        except Exception:
            Pylog.error("【获取赔率详情错误】：" + Pylog.exinfo())
            return "获取赔率详情错误"

    def quotaLimit_list(self, lotteryId=None):
        '''投注限制列表检索'''
        try:
            url = "http://" + self.host + "/ares-config/apis/quotaLimit/list"
            params = {"sideType": "2", "page": "1", "rows": "50", "lotteryId": lotteryId}
            resp = requests.get(url=url, headers=self.headers, params=params, timeout=15)
            Pylog.debug("【投注限制列表检索-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error("【投注限制列表检索错误】：" + Pylog.exinfo())
            return "投注限制列表检索错误"

    def quotaLimit_status(self, cid, status):
        '''投注限制停启用'''
        try:
            url = "http://" + self.host + "/ares-config/apis/quotaLimit/onStatus"
            params = {"id": cid, "status": status}
            resp = requests.post(url=url, headers=self.headers, params=params, timeout=15)
            Pylog.debug("【投注限制停启用-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error("【投注限制停启用错误】：" + Pylog.exinfo())
            return "投注限制停启用错误"

    def quotaLimit_statusAll(self, status):
        '''投注限制全部停启用'''
        try:
            clist = self.quotaLimit_list()
            clist = json.loads(clist)["data"]["rows"]
            for cid in clist:
                self.quotaLimit_status(cid["cid"], status)
            return "SUCCESS"
        except Exception:
            Pylog.error("【投注限制全部停启用错误】：" + Pylog.exinfo())
            return "投注限制全部停启用错误"

    def orderExp_list(self, lotteryId=None):
        '''异常方案设定列表'''
        try:
            url = "http://" + self.host + "/riskmanagementweb//apis/risk/orderExp/list"
            params = {"condition": json.dumps({"page": 1, "count": 50, "lotteryId": lotteryId, "sideType": 2})}
            resp = requests.get(url=url, headers=self.headers, params=params, timeout=15)
            Pylog.debug("【异常方案设定列表-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error("【异常方案设定列表错误】：" + Pylog.exinfo())
            return "异常方案设定列表错误"

    def orderExp_status(self, cid, status):
        '''异常方案设定停启用'''
        try:
            url = "http://" + self.host + "/riskmanagementweb//apis/risk/orderExp/updateOrderExpStatus"
            params = {"lotteryId": cid, "status": status}
            resp = requests.get(url=url, headers=self.headers, params=params, timeout=15)
            Pylog.debug("【异常方案设定停启用-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error("【异常方案设定停启用错误】：" + Pylog.exinfo())
            return "异常方案设定停启用错误"

    def orderExp_statusAll(self, status):
        '''
        :param status: 1停用， 0启用
        :return: 状态
        '''
        try:
            clist = self.orderExp_list()
            clist = json.loads(clist)["data"]["rows"]
            for cid in clist:
                self.orderExp_status(cid["lotteryId"], status)
            return "SUCCESS"
        except Exception:
            Pylog.error("【投注限制全部停启用错误】：" + Pylog.exinfo())
            return "投注限制全部停启用错误"


if __name__ == "__main__":
    Pylog()
    globalvars._init()
    Authors(types="control")
    LotteryConfig().orderExp_statusAll()
