# coding:utf-8
import requests
import json
import random
import time

from utils import utils
from config import globalvars
from action.apiaction import get_random
from auth.authors import Authors
from utils.pylog import Pylog

from action import memberaction
from action.control import lotteryConfig


class MemberBet:
    '''会员投注'''

    def __init__(self):
        self.config = globalvars.config()
        self.memberaction = memberaction.MemberAction()
        self.api = self.config.api
        owner = self.config.owner
        self.host = owner["env"]["host_mb"]
        self.headers = globalvars.get_value("headers_member")
        self.ordertotal = 0

    def getCurrentCode(self, lotteryId):
        '''获取当前期数'''
        try:
            # 排除秒秒彩
            if lotteryId not in [116, 118]:
                resp = requests.get(url="http://" + self.host + self.api["member"]["getpcode"],
                                    params={"lotteryId": lotteryId}, headers=self.headers, timeout=5)
                pdate = json.loads(resp.content)["data"][0]["pdate"]
                pcode = None
                currentTime = requests.get(url="http://{}/forseti/apid/serverCurrentTime".format(self.host),
                                           headers=self.headers, timeout=5).text
                Pylog.debug("【获取currentTime-resp】" + str(currentTime))
                currentTime = json.loads(currentTime)["data"]
                for i in json.loads(resp.text)["data"]:
                    startTime = i["startTime"]
                    endTime = i["endTime"]
                    if endTime > currentTime and currentTime > startTime:
                        pcode = i["pcode"]
                        break
                return [pdate, pcode]
            else:
                pdate = time.strftime("%Y%m%d", time.gmtime())
                return [pdate, ""]
        except Exception:
            Pylog.error("【获取当前期数错误】：" + Pylog.exinfo())
            return "获取当前期数错误"

    def do_randombet(self, lotteryid, datas, betAmount):
        '''投注'''

        successlist = []
        payoffAmount = 0
        try:
            pdata = self.getCurrentCode(lotteryid)
            pdate = pdata[0]
            pcode = pdata[1]
            for k, v in datas.items():
                dicts = {}
                dicts["play_id"] = k.split("|")[0]
                dicts["play_name"] = k.split("|")[1]
                dicts["content"] = v.split("|")[1]
                dicts["count"] = v.split("|")[0]

                # 兼容clion接口问题
                if int(dicts["count"]) == 0:
                    dicts["count"] = 1
                    dicts["content"] = dicts["play_name"].split("-")[1]
                # 替换model内容
                bet_data = self.config.model("member", "betinfo.json")
                bet_data["pcode"] = str(pcode)
                bet_data["pdate"] = str(pdate)
                bet_data["lotteryId"] = lotteryid
                bet_data["list"][0]["playId"] = dicts["play_id"]
                bet_data["list"][0]["betContent"] = dicts["content"]
                bet_data["list"][0]["betCount"] = dicts["count"]

                bet_data["list"][0]["multiple"] = betAmount / 100
                bet_data["amount"] = betAmount * int(dicts["count"])
                bet_data["list"][0]["betAmount"] = bet_data["amount"]
                datas = json.dumps(bet_data)

                self.headers["Content-Type"] = "application/json; charset=UTF-8"
                Pylog.debug("【投注-request】lotteryID:{} |".format(str(lotteryid)) + str(datas))
                resp = requests.post(url="http://" + self.host + self.api["member"]["bet"], data=datas,
                                     headers=self.headers, timeout=5)
                # Pylog.debug("【投注-resp】lotteryID:{} |".format(str(lotteryid)) + resp.text)
                respdata = json.loads(resp.text)
                Pylog.debug(
                    "【" + dicts["play_name"] + "】 " + str(resp.status_code) + "|" + str(respdata))
                if "orderId" in resp.text:
                    if len(respdata["data"]["orderId"]) > 0:
                        successlist.append(dicts["play_name"])
                        # 秒秒彩派彩计算
                        if lotteryid in [116, 118]:
                            for i in respdata["data"]["listOrder"]:
                                payoffAmount = payoffAmount + i["payoff"]
            globalvars.set_value("payoffAmount_"+str(lotteryid), payoffAmount)
            Pylog.info("【成功投注{}注,金额{}】{}".format(str(len(successlist)), str(betAmount), str(successlist)))
            return successlist
        except Exception:
            Pylog.error("【投注错误】：" + Pylog.exinfo())
            return "投注错误"

    def pre_bet(self, lotteryId):
        '''投注数据'''
        try:
            flag = "SUCCESS"
            plays = {}
            datas = get_random(lottery=lotteryId)
            keys = list(datas.keys())
            keys.sort()
            # ssc
            if lotteryId in [2, 12, 14, 26, 28, 32, 102, 112, 114]:
                keys = random.sample(keys[:28], 5) + random.sample(keys[28:78], 10) + \
                       random.sample(keys[78:], 5)

            # 11x5
            elif lotteryId in [4, 16, 18, 104]:
                keys = random.sample(keys[:29], 5) + random.sample(keys[29:84], 10) + \
                       random.sample(keys[84:], 5)

            # k3
            elif lotteryId in [6, 20, 22, 106]:
                keys = random.sample(keys[:7], 5) + random.sample(keys[7:35], 10) + \
                       random.sample(keys[35:], 5)

            # pk10
            elif lotteryId in [8, 24, 108]:
                keys = random.sample(keys[:55], 5) + random.sample(keys[55:72], 5) + \
                       random.sample(keys[72:], 10)

            # lhc
            elif lotteryId in [10, 110]:
                keys = random.sample(keys[:133], 10) + random.sample(keys[133:], 10)

            # 幸運28
            elif lotteryId in [30]:
                keys = random.sample(keys, 20)

            # mmc
            elif lotteryId in [116, 118]:
                keys = random.sample(keys, 20)

            for i in keys:
                plays[i] = datas[i]

            # 投注前查余额
            balance1 = self.memberaction.get_balance()
            balance1 = json.loads(balance1)["data"]["balance"]
            betAmount = random.randint(1, 10) * 100
            results = self.do_randombet(lotteryid=lotteryId, datas=plays, betAmount=betAmount)
            betAmount = betAmount * len(results)
            if lotteryId != 10:
                self.ordertotal = self.ordertotal + len(results)
            time.sleep(3)
            # 投注后查余额
            balance2 = self.memberaction.get_balance()
            balance2 = json.loads(balance2)["data"]["balance"]
            # 查看今日输赢
            todaymy = self.memberaction.get_balance(lotteryId=lotteryId)
            todaymy = json.loads(todaymy)["data"]["payoff"]
            #单个彩种派彩金额获取
            payoffAmount = globalvars.get_value("payoffAmount_" + str(lotteryId))
            Pylog.info("投注前后金额/今日输赢验证：投注前余额{},投注后余额{},投注金额{},派彩金额{},盈利金额{},今日输赢{}".format(str(balance1), str(balance2),
                                                                                      str(betAmount),
                                                                                      str(payoffAmount),
                                                                                      str(balance2 - balance1),
                                                                                      str(todaymy)))
            # if betAmount != balance1 - balance2 - self.payoffAmount:
            #     flag = "FAIL"
            #     Pylog.error("【餘額扣除驗證失敗！！！】")
            if todaymy != payoffAmount - betAmount:
                flag = "FAIL"
                Pylog.error("【今日輸贏驗證失敗！！！】")
                return "【今日輸贏驗證失敗！！！】"
            return "SUCCESS"
        except Exception:
            Pylog.error("【投注错误】：" + Pylog.exinfo())
            return "投注错误"

    def odds_compared(self, lotteryId, controlOdds):
        '''校验会员显示赔率'''
        try:
            flag = "SUCCESS"
            controlOddDict = {}
            controlOdds = json.loads(controlOdds)["data"]["itemVO"]
            for controlOdd in controlOdds:
                controlOddDict[controlOdd["playId"]] = controlOdd["payoff"]
            Pylog.debug("【主控展示赔率：】" + str(controlOddDict))

            modds = self.get_playsTree(lotteryId)
            modds = json.loads(modds)["data"]["childrens"]
            oddDatas = {}
            memberOddDict = utils.playsTreeRecursive(modds, oddDatas)
            Pylog.debug("【会员端展示赔率：】" + str(memberOddDict))
            for odd in list(memberOddDict.keys()):
                if memberOddDict[odd] != controlOddDict[odd]:
                    flag = "FAIL"
            return flag
        except Exception:
            Pylog.error("【校验会员显示赔率错误】：" + Pylog.exinfo())
            return "校验会员显示赔率错误"

    def get_playsTree(self, lotteryId):
        '''获取玩法树'''
        try:
            url = "http://" + self.host + "/forseti/api/playsTree"
            resp = requests.get(url=url, headers=self.headers,
                                params={"lotteryId": lotteryId, "maxUpdateTime": None})
            Pylog.debug("【获取玩法树-resp】：" + str(resp.status_code))
            return resp.text
        except Exception:
            Pylog.error("【获取玩法树错误】：" + Pylog.exinfo())
            return "获取玩法树错误"

if __name__ == "__main__":
    Pylog()
    globalvars._init()
    Authors(types="member")
    Authors(types="control")
    memberBet = MemberBet()
    ss = memberBet.get_playsTree(10)
    print(ss)

