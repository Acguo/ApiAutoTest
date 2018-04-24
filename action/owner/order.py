# coding:utf-8
import requests
import json

from utils.pylog import Pylog
from utils import utils
from config import globalvars
from auth.authors import Authors

class Order():
    '''方案管理'''
    def __init__(self, auth=None):
        self.config = globalvars.config()
        self.api = self.config.api
        owner = self.config.owner
        self.host = owner["env"]["host_mb"]
        self.headers = globalvars.get_value("headers_owner")
        self.headers["Origin"] = owner["env"]["origin_yz"]

    def order_todaylist(self, memberName, lotteryId=None):
        '''获取今日方案'''
        try:
            url = "http://" + self.host + self.api["owner"]["order_todylist"]
            # self.headers.pop("Content-Type")
            datas = self.config.model("owner", "orderlist.json")
            datas["memberName"] = memberName
            datas["condition"]["memberName"] = memberName
            datas["condition"]["lotteryId"] = lotteryId
            datas["condition"] = json.dumps(datas["condition"])
            resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
            Pylog.debug("【今日方案-resp】" + str(resp.text))
            return str(resp.text)
        except Exception:
            Pylog.error("【获取今日方案错误】：" + Pylog.exinfo())
            return "获取今日方案错误"

    def order_historylist(self):
        '''历史方案'''
        url = "http://" + self.host + self.api["owner"]["order_historylist"]
        datas = self.config.model("owner", "orderlist.json")
        datas["condition"]["betStartTime"] = utils.datetime_timestamp('2018-02-05 00:00:00') * 1000
        datas["condition"]["betEndTime"] = utils.datetime_timestamp('2018-02-05 23:59:59') * 1000
        datas["condition"] = json.dumps(datas["condition"])
        resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【历史方案-request】" + str(datas))
        Pylog.info("【历史方案-resp】" + str(resp.text))
        return str(resp.text)

    def prizeNumber(self):
        '''开奖历史'''
        url = "http://" + self.host + self.api["owner"]["prizeNumber"]
        datas = self.config.model("owner", "prizeNumber.json")
        resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【开奖历史-resp】" + str(resp.text))
        return str(resp.text)

    def order_repeal(self, memberName):
        '''业主撤单'''
        try:
            repealDict = {}
            flag = "SUCCESS"
            url = "http://" + self.host + "/hermes/apis/order/management/repeal"
            orderlist = self.order_todaylist(memberName)
            orderlist = json.loads(orderlist)["data"]["rows"]
            for i in orderlist:
                repealDict[i["lotteryId"]] = i["orderId"]
            for cid in list(repealDict.values()):
                resp = requests.post(url=url, headers=self.headers, params={"orderId": cid}, timeout=15)
                Pylog.debug("【业主撤单-resp】" + resp.text)
                if "true" not in resp.text:
                    flag = "FAIL"
            return flag
        except Exception:
            Pylog.error("【业主撤单错误】：" + Pylog.exinfo())
            return "业主撤单错误"

if __name__ == "__main__":
    Pylog()
    globalvars._init()
    Authors("owner")
    order = Order()
    ss = order.order_repeal("vct_hkjc_02")
    print(ss)