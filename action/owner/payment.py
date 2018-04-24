# coding:utf-8
import requests
import json
from auth.authors import Authors
from config import globalvars
from utils.pylog import Pylog


class Payment:
    '''资金管理'''
    def __init__(self):
        self.config = globalvars.config()
        self.api = self.config.api
        owner = self.config.owner
        self.host = owner["env"]["host_mb"]
        self.headers = globalvars.get_value("headers_owner")
        self.headers["Origin"] = owner["env"]["origin_yz"]

    def chargeCmy_list(self, memberName=None):
        '''公司入款列表'''
        url = "http://" + self.host + self.api["owner"]["chargeCmy_list"]
        datas = {"memberName": memberName, "page": 1, "rows": 15}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.debug("【公司入款列表-request】" + str(datas))
        Pylog.info("【公司入款列表-resp】" + str(resp.text))
        return str(resp.text)

    def draw_list(self, memberName=None):
        '''会员出款列表'''
        try:
            url = "http://" + self.host + self.api["owner"]["draw_list"]
            datas = {"memberName": memberName, "page": 1, "rows": 15}
            resp = requests.get(url=url, params=datas, headers=self.headers)
            Pylog.debug("【会员出款审核列表搜索-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error("【会员出款审核列表搜索错误】：" + Pylog.exinfo())
            return "会员出款审核列表搜索错误"

    def draw_audit(self, id, state):
        '''会员出款审核'''
        try:
            url = "http://" + self.host + self.api["owner"]["draw_audit"]
            datas = {"id": id, "state": state}
            resp = requests.get(url=url, params=datas, headers=self.headers)
            Pylog.debug("【会员出款审核-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error("【会员出款审核错误】：" + Pylog.exinfo())
            return "会员出款审核错误"

    def trade_statList(self):
        '''出入款账目汇总查询'''
        url = "http://" + self.host + self.api["owner"]["trade_statList"]
        datas = {"endTime": 1519833599000, "startTime": 1519833600000}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.info("【出入款账目汇总查询-resp】" + str(resp.text))
        return str(resp.text)

    def offline_statList(self, endTime=1522511999000, startTime=1519833600000):
        '''出入款账目汇总_公司入款查询'''
        url = "http://" + self.host + self.api["owner"]["offline_statList"]
        datas = {"endTime": endTime, "page": 1, "rows": 15, "startTime": startTime}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.info("【出入款账目汇总_公司入款查询-resp】" + str(resp.text))
        return str(resp.text)

    def offline_detail(self, endTime=1522511999000, startTime=1519833600000, cardNo=6225888899990000777):
        '''出入款账目汇总_公司入款详情查询'''
        url = "http://" + self.host + self.api["owner"]["offline_detail"]
        datas = {"endTime": endTime, "page": 1, "rows": 15, "startTime": startTime, "cardNo": cardNo}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.debug("【出入款账目汇总_公司入款详情查询-request】" + str(datas))
        Pylog.info("【出入款账目汇总_公司入款详情查询-resp】" + str(resp.text))
        return str(resp.text)

    def online_statList(self, endTime=1522511999000, startTime=1519833600000):
        '''出入款账目汇总_线上入款查询'''
        url = "http://" + self.host + self.api["owner"]["online_statList"]
        datas = {"endTime": endTime, "page": 1, "rows": 15, "startTime": startTime}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.info("【出入款账目汇总_线上入款查询-resp】" + str(resp.text))
        return str(resp.text)

    def online_detail(self, endTime=1522511999000, startTime=1519833600000, merchantNo=1063, merchantName='E时代-WAPQQ'):
        '''出入款账目汇总_线上入款详情查询'''
        url = "http://" + self.host + self.api["owner"]["online_detail"]
        datas = {"endTime": endTime, "page": 1, "rows": 15, "startTime": startTime, "merchantNo": merchantNo,
                 "merchantName": merchantName}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.debug("【出入款账目汇总_线上入款详情查询-request】" + str(datas))
        Pylog.info("【出入款账目汇总_线上入款详情查询-resp】" + str(resp.text))
        return str(resp.text)

    def chargeanddraw_statList(self, searchType=5):
        '''出入款账目汇总_人工入款和会员出款扣款查询
            searchType:
                5：人工入款
                6：会员出款扣款
                8：人工提出
                10：给予优惠
        '''
        url = "http://" + self.host + self.api["owner"]["chargeanddraw_statList"]
        datas = {"endTime": 1522511999000, "page": 1, "rows": 15, "startTime": 1519833600000, "searchType": searchType}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        if searchType == 5:
            Pylog.info("【出入款账目汇总_人工入款查询-resp】" + str(resp.text))
        elif searchType == 6:
            Pylog.info("【出入款账目汇总_会员出款扣款查询-resp】" + str(resp.text))
        return str(resp.text)

    def syscharge_detail(self):
        '''出入款账目汇总_人工存款详情查询'''
        url = "http://" + self.host + self.api["owner"]["syscharge_detail"]
        datas = {"endTime": 1522511999000, "page": 1, "rows": 15, "startTime": 1519833600000, "actionType": 10}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.info("【出入款账目汇总_人工存款详情查询-resp】" + str(resp.text))
        return str(resp.text)

    def debit_detail(self):
        '''出入款账目汇总_手续费扣除详情查询'''
        url = "http://" + self.host + self.api["owner"]["debit_detail"]
        datas = {"endTime": 1522511999000, "page": 1, "rows": 15, "startTime": 1517414400000, "actionType": 40}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.info("【出入款账目汇总_手续费扣除详情查询-resp】" + str(resp.text))
        return str(resp.text)

    def draw_statList(self, endTime=1522511999000, startTime=1519833600000):
        '''出入款账目汇总_会员出款查询'''
        url = "http://" + self.host + self.api["owner"]["draw_statList"]
        datas = {"endTime": endTime, "page": 1, "rows": 15, "startTime": startTime}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.info("【出入款账目汇总_会员出款查询-resp】" + str(resp.text))
        return str(resp.text)

    def draw_detail(self, endTime=1522511999000, startTime=1519833600000, memberName='justsoso666'):
        '''出入款账目汇总_会员出款详情查询'''
        url = "http://" + self.host + self.api["owner"]["draw_detail"]
        datas = {"endTime": endTime, "page": 1, "rows": 15, "startTime": startTime, "memberName": memberName}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.debug("【出入款账目汇总_会员出款详情查询-request】" + str(datas))
        Pylog.info("【出入款账目汇总_会员出款详情查询-resp】" + str(resp.text))
        return str(resp.text)

    def sysdraw_detail(self):
        '''出入款账目汇总_人工提出详情查询'''
        url = "http://" + self.host + self.api["owner"]["sysdraw_detail"]
        datas = {"endTime": 1522511999000, "page": 1, "rows": 15, "startTime": 1519833600000, "actionType": 20}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.info("【出入款账目汇总_人工提出详情查询-resp】" + str(resp.text))
        return str(resp.text)

    def cashback_statList(self):
        '''出入款账目汇总_给予返水查询'''
        url = "http://" + self.host + self.api["owner"]["cashback_statList"]
        datas = {"endTime": 1522511999000, "page": 1, "rows": 15, "startTime": 1519833600000}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.info("【出入款账目汇总_给予返水查询-resp】" + str(resp.text))
        return str(resp.text)

    def backwater_detail(self):
        '''出入款账目汇总_给予返水详情查询'''
        url = "http://" + self.host + self.api["owner"]["backwater_detail"]
        datas = {"endTime": 1522511999000, "page": 1, "rows": 15, "startTime": 1519833600000, "actionType": 20}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.info("【出入款账目汇总_给予返水详情查询-resp】" + str(resp.text))
        return str(resp.text)

    def discount_detail(self):
        '''出入款账目汇总_给予优惠详情查询'''
        url = "http://" + self.host + self.api["owner"]["discount_detail"]
        datas = {"endTime": 1522511999000, "page": 1, "rows": 15, "startTime": 1519833600000, "actionType": 3}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.info("【出入款账目汇总_给予优惠详情查询-resp】" + str(resp.text))
        return str(resp.text)

    def offline_chargeList(self, memberName, state=0):
        '''公司入款审核列表搜索
            state：
                0：待处理
                5：已锁定
        '''
        try:
            url = "http://" + self.host + self.config.api["owner"]["offline_chargeList"]
            datas = {"page": 1, "rows": 15, "state": state, "memberName": memberName}
            Pylog.debug("【公司入款审核列表搜索-request】" + str(datas))
            resp = requests.get(url=url, params=datas, headers=self.headers, timeout=5)
            Pylog.debug("【公司入款审核列表搜索-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【公司入款审核列表搜索错误】：" + Pylog.exinfo())
            return "公司入款审核列表搜索错误"

    def offline_audit(self, id, state):
        '''公司入款审核相关操作
            state：
                5：锁定
                4: 通过
                3：拒绝
        '''
        try:
            url = "http://" + self.host + self.api["owner"]["offline_audit"]
            datas = {"id": id, "state": state}
            resp = requests.get(url=url, params=datas, headers=self.headers)
            Pylog.debug("【公司入款审核resp】" + str(resp.text))
            return str(resp.text)
        except Exception:
            Pylog.error("【公司入款审核错误】：" + Pylog.exinfo())
            return "公司入款审核错误"

    def online_chargeList(self, memberName=None, state=None):
        '''线上入款审核列表搜索'''
        try:
            url = "http://" + self.host + self.api["owner"]["online_chargeList"]
            datas = {"page": 1, "rows": 15, "state": state, "memberName": memberName}
            resp = requests.get(url=url, params=datas, headers=self.headers)
            Pylog.debug("【线上入款审核列表搜索-resp】" + str(resp.text))
            return str(resp.text)
        except Exception:
            Pylog.error("【线上入款审核列表搜索错误】：" + Pylog.exinfo())
            return "线上入款审核列表搜索错误"

    def online_audit(self, id, state):
        '''线上入款审核相关操作'''
        try:
            url = "http://" + self.host + self.api["owner"]["online_audit"]
            datas = {"id": id, "state": state}
            resp = requests.get(url=url, params=datas, headers=self.headers)
            Pylog.debug("【线上入款审核核-resp】" + str(resp.text))
            return str(resp.text)
        except Exception:
            Pylog.error("【线上入款审核错误】：" + Pylog.exinfo())
            return "线上入款审核错误"

    def member_audit(self, account):
        '''即时稽核查询'''
        try:
            url = "http://" + self.host + self.api["owner"]["member_audit"]
            datas = {"account": account}
            resp = requests.get(url=url, params=datas, headers=self.headers)
            Pylog.debug("【即时稽核查询查询-resp】" + str(resp.text))
            return str(resp.text)
        except Exception:
            Pylog.error("【即时稽核查询错误】：" + Pylog.exinfo())
            return "即时稽核查询错误"

    def balance_get(self, memberName):
        '''人工存入账号信息查询'''
        try:
            url = "http://" + self.host + self.api["owner"]["balance_get"]
            datas = {"memberName": memberName}
            resp = requests.get(url=url, params=datas, headers=self.headers)
            Pylog.debug("【人工存入账号信息查询-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【人工存入账号信息查询错误】：" + Pylog.exinfo())
            return "人工存入账号信息查询错误"

    def system_charge(self, memberName, chgtype):
        '''人工存入'''
        try:
            url = "http://" + self.host + self.api["owner"]["system_charge"]
            memberId = self.balance_get(memberName)
            memberId = json.loads(memberId)["data"]["memberId"]
            datas = {"memberName": memberName, "memberId": memberId, "actionType": 10, "chargeAmount": 10000,
                     "chargeRemark": "auto备注{}1".format(chgtype), "depDiscount": 1000,
                     "depRemark": "auto备注{}2".format(chgtype), "remDiscount": 0,
                     "remRemark": None, "discountAudit": "2", "ifNormalAudit": 1}
            if "活动优惠" == chgtype:
                datas = {"memberName": memberName, "memberId": memberId, "actionType": 13,
                         "chargeAmount": 10000, "chargeRemark": "auto备注{}".format(chgtype), "depDiscount": 0,
                         "depRemark": None, "remDiscount": 0, "remRemark": None,
                         "discountAudit": "2", "ifNormalAudit": 0}
            elif "其他入款" == chgtype:
                datas = {
                    "memberName": memberName, "memberId": memberId, "actionType": 17,
                    "chargeAmount": 10000, "chargeRemark": "auto备注其他入款",
                    "depDiscount": 0, "depRemark": None, "remDiscount": 0,
                    "remRemark": None, "discountAudit": None, "ifNormalAudit": 1}

            Pylog.debug("【人工存入-request】" + str(datas))
            resp = requests.post(url=url, data=json.dumps(datas), headers=self.headers)
            Pylog.debug("【人工存入-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【人工存入账号信息查询错误】：" + Pylog.exinfo())
            return "人工存入账号信息查询错误"

    def system_draw(self, memberName, drawtype):
        '''人工提出'''
        try:
            url = "http://" + self.host + self.api["owner"]["system_draw"]
            memberId = self.balance_get(memberName)
            memberId = json.loads(memberId)["data"]["memberId"]
            datas = {
                "memberName": memberName, "memberId": memberId, "actionType": 21, "drawAmount": 10000,
                "drawRemark": "auto备注{}".format(drawtype), "cleanNormalAudit": 1, "cleanDiscountAudit": 1}
            if drawtype == "其他出款":
                datas["actionType"] = 26
                datas["cleanNormalAudit"] = 2
                datas["cleanDiscountAudit"] = 2
            Pylog.debug("【人工提出-request】" + str(datas))
            resp = requests.post(url=url, data=json.dumps(datas), headers=self.headers)
            Pylog.debug("【人工提出-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error("【人工提出错误】：" + Pylog.exinfo())
            return "人工提出错误"

    def chargeanddraw_record(self, membername, tradeType):
        '''人工存提记录'''
        try:
            url = "http://" + self.host + self.api["owner"]["chargeanddraw_record"]
            tradeTypeId = 8 if tradeType == "人工提出" else 5
            datas = {"memberName": membername, "page": 1, "rows": 15, "tradeType": tradeTypeId}
            resp = requests.get(url=url, params=datas, headers=self.headers)
            Pylog.debug("【人工提出记录-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error("【人工存提记录错误】：" + Pylog.exinfo())
            return "人工存提记录错误"

    def cashFlow_list(self, memberAccount):
        '''金流查询'''
        try:
            url = "http://" + self.host + self.api["owner"]["cashFlow_list"]
            datas = {"memberAccount": memberAccount, "page": 1, "rows": 15, "tradeAction": -1}
            resp = requests.get(url=url, params=datas, headers=self.headers)
            Pylog.debug("【金流查询-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error("【人工存提记录错误】：" + Pylog.exinfo())
            return "人工存提记录错误"

    def mem_cash_back_details(self, type=2, account=None, status=1):
        '''会员返水管理'''
        url = "http://" + self.host + self.api["owner"]["mem_cash_back_details"]
        datas = {"account": account, "page": 1, "rows": 15, "status": status, "type": type}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.debug("【会员返水管理-request】" + str(datas))
        Pylog.info("【会员返水管理-resp】" + str(resp.text))
        return str(resp.text)

    def rebateProgram_view(self, cid=23):
        '''查看返水方案'''
        url = "http://" + self.host + self.api["owner"]["rebateProgram_view"]
        datas = {"cid": cid}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.debug("【查看返水方案-request】" + str(datas))
        Pylog.info("【查看返水方案-resp】" + str(resp.text))
        return str(resp.text)

    def r_com_current_pcode_summary(self, agentName='default'):
        '''搜索退佣当期报表'''
        url = "http://" + self.host + self.api["owner"]["r_com_current_pcode_summary"]
        datas = {"agentName": agentName, "page": 1, "rows": 15}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.debug("【搜索退佣当期报表-request】" + str(datas))
        Pylog.info("【搜索退佣当期报表-resp】" + str(resp.text))
        return str(resp.text)

    def retirement_view(self, cid=24):
        '''查看退佣方案'''
        url = "http://" + self.host + self.api["owner"]["retirement_view"]
        tmp = Payment().r_com_current_pcode_summary()
        dictTmp = json.loads(tmp)
        cid = dictTmp['data']['rows'][0]['rcomId']
        datas = {"cid": cid}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.debug("【查看退佣方案-request】" + str(datas))
        Pylog.info("【查看退佣方案-resp】" + str(resp.text))
        return str(resp.text)

    def r_com_month_bill_detail(self, rComPcodeId=20180227823):
        '''退佣账单详情'''
        url = "http://" + self.host + self.api["owner"]["r_com_month_bill_detail"]
        datas = {"page": 1, "rComPcodeId": rComPcodeId, "rows": 15}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.debug("【退佣账单详情-request】" + str(datas))
        Pylog.info("【退佣账单详情-resp】" + str(resp.text))
        return str(resp.text)


if __name__ == "__main__":
    Pylog()
    globalvars._init()
    Authors("owner")
    payment = Payment()
    payment.system_draw("auto_pt2_10", "其他出款")
