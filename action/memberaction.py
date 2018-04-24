# coding:utf-8
import requests
import json
import random
import time
from concurrent.futures import ThreadPoolExecutor
from config import globalvars
from action.apiaction import get_random
from auth.authors import Authors
from utils.pylog import Pylog


class MemberAction():
    def __init__(self):
        self.config = globalvars.config()
        self.api = self.config.api
        owner = self.config.owner
        self.host = owner["env"]["host_mb"]
        if globalvars.get_value("headers_member") == None:
            self.headers = {
                "Origin": owner["env"]["origin_mb"],
                "Accept": "application/json",
                "Content-Type": "application/json; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "clientId": "BH80xYtfSel9Yr2p_1uQKi8N7Fg8mBVhlCqJROWL",
                "Authorization": "Basic d2ViX2FwcDo="
            }
        else:
            self.headers = globalvars.get_value("headers_member")

    def do_testplay(self):
        '''试玩'''
        try:
            resp = requests.post(url="http://" + self.host + self.api["member"]["testlogin"], headers=self.headers,
                                 timeout=15)
            Pylog.debug("【试玩-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "试玩错误"

    def getconfig_reg(self):
        '''获取注册配置'''
        try:
            url = "http://" + self.host + "/forseti/apid/config/registerConfig?regType=1"
            resp = requests.get(url=url, headers=self.headers)
            Pylog.debug("【获取注册配置-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【获取注册配置错误】:" + Pylog.exinfo())
            return "获取注册配置错误"

    def createMember(self, username):
        '''注册'''
        try:
            url = "http://" + self.host + self.api["member"]["CreateMember"]
            datas = self.config.model(role="member", filename="CreateMember.json")
            datas["login"] = username
            Pylog.debug("【注册-request】" + str(datas))
            resp = requests.post(url=url, data=json.dumps(datas), headers=self.headers, timeout=15)
            Pylog.debug("【注册-resp】" + str(resp.text))
            if "FAILED" in json.loads(resp.text)["err"]:
                if "用户名已被注册" in json.loads(resp.text)["cnMsg"]:
                    Pylog.info("【使用 {} 登陆】".format(username))
                    results = self.login(username)
                    return results
                else:
                    return resp.text
            else:
                return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "注册错误"

    def login(self, userName):
        '''会员登陆'''
        try:
            url = "http://" + self.host + self.api["member"]["login"]
            datas = self.config.model("member", "login.json")
            datas["username"] = datas["username"].replace("victor", userName)
            self.headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
            self.headers["Authorization"] = "Basic d2ViX2FwcDo="
            Pylog.debug("【登陆-request】" + str(datas))
            resp = requests.post(url=url, data=datas, headers=self.headers, timeout=15)
            Pylog.debug("【登陆-resp】" + resp.text)
            self.headers["Authorization"] = str(json.loads(resp.text)["data"]["token_type"]) + " " + str(
                json.loads(resp.text)["data"]["access_token"])
            self.headers["Content-Type"] = "application/json; charset=UTF-8"
            Pylog.info("【登陆鉴权member】 | " + userName + " " + str(datas["password"]))
            globalvars.set_value("headers_member", self.headers)
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "会员登陆错误"

    def charge_client(self):
        '''获取入款配置信息'''
        try:
            url = "http://" + self.host + "/forseti/api/pay/receiptClient"
            resp = requests.get(url=url, headers=self.headers)
            Pylog.debug("【获取入款配置信息-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取入款配置信息错误"

    def charge_walletpay(self, accountType, money):
        '''会员钱包支付'''
        try:
            url_client = "http://" + self.host + "/forseti/api/pay/getWalletPayAccount"
            url = "http://" + self.host + "/forseti/api/pay/offlineOrder"
            cientInfo = requests.get(url=url_client, headers=self.headers)
            cientInfo = json.loads(cientInfo.text)["data"][accountType - 1]
            datas = {"chargeAmount": money,
                     "source": 2,
                     "cardNo": cientInfo["accountNo"],
                     "payConfigId": cientInfo["id"],
                     "payMethod": accountType + 7,
                     "cardOwnerName": cientInfo["accountName"],
                     "depositorName": "autotest",
                     "flowType": 1}
            self.headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
            Pylog.debug("【会员钱包支付-request】" + str(datas))
            resp = requests.post(url=url, headers=self.headers, data=datas)
            Pylog.debug("【会员钱包支付-resp】" + resp.text)
            self.headers["Content-Type"] = "application/json; charset=UTF-8"
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "钱包支付错误"

    def charge_online(self, client, money):
        '''线上入款'''
        try:
            url = "http://" + self.host + "/forseti/api/pay/rapidOrder"
            clist = self.charge_client()
            clist = json.loads(clist)["data"]
            for c in clist:
                if client in c["rsName"]:
                    rapidType = c["rsNameId"]
            datas = {"chargeAmount": money,
                     "source": 2,
                     "rapidType": rapidType,
                     "paymentType": "",
                     "paymentTypeName": "",
                     "realName": "",
                     "flowType": 4}
            Pylog.debug("【线上入款-request】" + str(datas))
            self.headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
            resp = requests.post(url=url, headers=self.headers, data=datas)
            Pylog.debug("【线上入款-resp】" + resp.text)
            self.headers["Content-Type"] = "application/json; charset=UTF-8"
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "线上入款错误"

    def charge_company(self, money):
        '''公司入款'''
        try:
            url_bank = "http://" + self.host + "/forseti/api/payment/incomeBank"
            url = "http://" + self.host + self.api["member"]["charge_company"]
            datas = self.config.model(role="member", filename="chargeCmy.json")

            # 获取公司入款账号
            resp = requests.get(url=url_bank, headers=self.headers, timeout=15)
            Pylog.debug("【公司入款-获取公司入款账号-resp】" + resp.text)
            resp = json.loads(resp.text)["data"]
            datas.update({"bankCode": resp["bankCode"],
                          "cardNo": resp["cardNo"],
                          "registerBankInfo": resp["registerBankInfo"],
                          "cardOwnerName": resp["cardOwnerName"],
                          "chargeAmount": money})
            self.headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
            Pylog.debug("【公司入款-request】" + str(datas))
            resp = requests.post(url=url, data=datas, headers=self.headers, timeout=15)
            Pylog.debug("【公司入款-resp】" + str(resp.text))
            self.headers["Content-Type"] = "application/json; charset=UTF-8"
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "公司入款错误"

    def saveMemberBank(self):
        '''会员第一次提款绑卡'''
        try:
            url = "http://" + self.host + "/forseti/api/payment/memberBank"
            datas = self.config.model(role="member", filename="saveMemberBank.json")
            bankcard = str(time.time()).replace(".", "")
            datas["bankCard"] = bankcard
            globalvars.set_value("bind_data", datas)
            self.headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
            Pylog.debug("【绑卡-request】" + str(datas))
            resp = requests.post(url=url, data=datas, headers=self.headers, timeout=15)
            Pylog.debug("【绑卡-resp】" + resp.text)
            self.headers["Content-Type"] = "application/json; charset=UTF-8"
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "绑卡错误"

    def changeDrawPwd(self, oldpwd, newpwd):
        '''更改取款密码'''
        try:
            url = "http://" + self.host + "/forseti/api/pay/passwd"
            self.headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
            resp = requests.post(url=url, data={"oldPassword": oldpwd, "tradePassword": newpwd}, headers=self.headers,
                                 timeout=15)
            Pylog.debug("【更改取款密码-resp】" + resp.text)
            self.headers["Content-Type"] = "application/json; charset=UTF-8"
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "更改取款密码错误"

    def drawOrder(self, money, pwd):
        '''取款'''
        try:
            url = "http://" + self.host + "/forseti/api/pay/drawOrder"
            datas = globalvars.get_value("bind_data")
            datas.update({"applyAmount": money, "tradePassword": pwd, "source": "2"})
            self.headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
            Pylog.debug("【取款-request】" + str(datas))
            resp = requests.post(url=url, data=datas, headers=self.headers, timeout=15)
            Pylog.debug("【取款-resp】" + str(resp.text))
            return resp.text
        except:
            Pylog.error(Pylog.exinfo())
            return "取款错误"

    def get_carousel(self):
        "获取轮播图信息"
        try:
            url = "http://" + self.host + "/forseti/apid/cms/carousel"
            resp = requests.get(url=url, headers=self.headers)
            Pylog.debug("【获取轮播图信息-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取轮播图信息错误"

    def get_msg(self):
        '''获取站内信'''
        try:
            url = "http://" + self.host + "/forseti/apid/cms/msg/list?sourceType=2&page=1&rows=5"
            url_read = "http://" + self.host + "/forseti/apid/cms/msg/read?sourceType=2"
            url_status = "http://" + self.host + "/forseti/apid/cms/msg/status?sourceType=2"
            requests.get(url=url_status, headers=self.headers)
            requests.get(url=url_read, headers=self.headers)
            resp = requests.get(url=url, headers=self.headers)
            Pylog.debug("【获取站内信-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取站内信错误"

    def get_popText(self):
        '''获取首页弹屏'''
        try:
            url = "http://" + self.host + "/forseti/apid/cms/popText"
            resp = requests.get(url=url, headers=self.headers)
            Pylog.debug("【获取首页弹屏-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取首页弹屏错误"

    def get_notice(self):
        '''获取首页公告'''
        try:
            url = "http://" + self.host + "/forseti/apid/cms/notices?sideType=2&appid=bcappid02"
            resp = requests.get(url=url, headers=self.headers)
            Pylog.debug("【获取首页公告-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取首页公告错误"

    def get_activity(self, cid):
        '''获取优惠活动'''
        try:
            url = "http://" + self.host + "/forseti/apid/cms/activityInfo?cid={}".format(str(cid))
            resp = requests.get(url=url, headers=self.headers)
            Pylog.debug("【获取优惠活动-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取优惠活动错误"

    def get_balance(self, lotteryId=None):
        '''获取余额'''
        try:
            url = "http://" + self.host + "/hermes/api/balance/get"
            resp = requests.get(url=url, headers=self.headers, params={"lotteryId": lotteryId})
            Pylog.debug("【获取余额-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取余额错误"

    def get_tradeList(self, searchType=1):
        '''获取账户明细'''
        try:
            url = "http://" + self.host + "/forseti/api/pay/tradeDayList?searchType={}&page=1&rows=10".format(
                searchType)
            url1 = "http://" + self.host + "/forseti/api/pay/tradeList"
            pdate = requests.get(url=url, headers=self.headers)
            pdate = json.loads(pdate.text)["data"][0]["pdate"]
            resp = requests.get(url=url1, headers=self.headers,
                                params={"searchType": searchType, "page": 1, "rows": 50, "pdate": pdate})
            Pylog.debug("【获取账户明细-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取账户明细错误"

    def get_judge(self):
        '''获取稽核数据'''
        try:
            url = "http://" + self.host + "/forseti/api/pay/drawOrder/judge"
            resp = requests.post(url=url, headers=self.headers)
            Pylog.debug("【获取稽核数据-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取稽核数据错误"

    def apid_lotterys(self):
        '''获取彩种排序'''
        try:
            url = "http://" + self.host + self.config.api["member"]["apid_lotterys"]
            datas = {"sideType": 2}
            resp = requests.get(url=url, headers=self.headers, params=datas)
            Pylog.debug("【获取彩种排序-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取彩种排序错误"

    def config_custConfig(self):
        '''获取客服地址'''
        try:
            url = "http://" + self.host + self.config.api["member"]["config_custConfig"]
            resp = requests.get(url=url, headers=self.headers)
            Pylog.debug("【获取客服地址-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取客服地址错误"

    def config_appConfig(self):
        '''获取app地址'''
        try:
            url = "http://" + self.host + self.config.api["member"]["config_appConfig"]
            resp = requests.get(url=url, headers=self.headers)
            Pylog.debug("【获取app地址-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取app地址错误"

    def cms_site(self):
        '''获取站点信息'''
        try:
            url = "http://" + self.host + self.config.api["member"]["cms_site"]
            resp = requests.get(url=url, headers=self.headers)
            Pylog.debug("【获取站点信息-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取站点信息错误"

    def cms_copyright(self, type=1, code='BT01'):
        '''获取网站说明文案'''
        try:
            url = "http://" + self.host + self.config.api["member"]["cms_copyright"]
            datas = {"type": type, "code": code}
            resp = requests.get(url=url, headers=self.headers, params=datas)
            Pylog.debug("【获取网站说明文案-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取网站说明文案错误"

    def cms_activityInfo(self, cid):
        '''获取优惠活动信息'''
        try:
            url = "http://" + self.host + self.config.api["member"]["cms_activityInfo"]
            datas = {"cid": cid}
            resp = requests.get(url=url, headers=self.headers, params=datas)
            Pylog.debug("【获取优惠活动信息-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取优惠活动信息错误"

    def cms_carousel(self):
        '''获取轮播图'''
        try:
            url = "http://" + self.host + self.config.api["member"]["cms_carousel"]
            resp = requests.get(url=url, headers=self.headers)
            Pylog.debug("【获取轮播图-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取轮播图错误"

    def cms_notice(self):
        '''获取公告'''
        try:
            url = "http://" + self.host + self.config.api["member"]["cms_notices"]
            resp = requests.get(url=url, headers=self.headers)
            Pylog.debug("【获取公告-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取公告错误"

    def cms_popText(self):
        '''获取首页弹屏'''
        try:
            url = "http://" + self.host + self.config.api["member"]["cms_popText"]
            resp = requests.get(url=url, headers=self.headers)
            Pylog.debug("【获取首页弹屏-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取首页弹屏错误"

    def msg_list(self):
        '''获取站内信'''
        # 设置Authorization
        # self.headers["Authorization"] = self.owner["env"]["msg_Author"]
        try:
            url = "http://" + self.host + self.config.api["member"]["msg_list"]
            datas = {"sourceType": 2, "page": 1, "rows": 5}
            resp = requests.get(url=url, headers=self.headers, params=datas)
            Pylog.debug("【获取站内信-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取站内信错误"

    def orderlist_get(self):
        '''获取今日所有注单'''
        try:
            pdate = globalvars.get_value("pdate")
            url = "http://" + self.host + "/forseti/api/orders/orderList"
            datas = {"page": 1, "pageSize": 600, "searchType": 1, "statusType": 1, "lotteryId": "0", "sideType": "2",
                     "pdate": pdate}
            resp = requests.post(url=url, headers=self.headers, data=json.dumps(datas))
            Pylog.debug("【获取今日所有注单-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error(Pylog.exinfo())
            return "获取今日所有注单错误"


if __name__ == "__main__":
    Pylog()
    globalvars._init()
    memberaction = MemberAction()
    for i in range(0, 100):
        memberaction.login("vct_hkjc888_06")
        ss = memberaction.charge_client()
        if len(json.loads(ss)["data"]) is None:
            print(ss)
