# coding:utf-8
import requests
import json

from pylog import Pylog
from utils.utils import Utils
from auth.authors import Authors

class Statics():
    '''统计查询'''
    def __init__(self, auth=None):
        if auth == None:
            self.auth = Authors(types="owner")
        else:
            self.auth = auth
        self.host = self.auth.config.owner["env"]["host_yz"]
        self.headers = self.auth.headers

    def statics_agent(self, endTime=1519833599000, startTime=1517414400000, agent='default'):
        '''代理统计报表搜索'''
        url = "http://" + self.host + self.auth.config.api["owner"]["statics_agent"]
        datas = {"endTime": endTime, "page": 1, "rows": 15, "startTime": startTime, "agent": agent, "sideType": 2}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【代理统计报表搜索-request】" + str(datas))
        Pylog.info("【代理统计报表搜索-resp】" + str(resp.text))
        return str(resp.text)

    def statics_member(self, endTime=1519833599000, startTime=1517414400000, agentId=None):
        '''会员统计报表搜索'''
        url = "http://" + self.host + self.auth.config.api["owner"]["statics_member"]
        datas = {"endTime": endTime, "page": 1, "rows": 15, "startTime": startTime, "agentId": agentId}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【会员统计报表搜索-request】" + str(datas))
        Pylog.info("【会员统计报表搜索-resp】" + str(resp.text))
        return str(resp.text)

    def search_member(self, endTime=1519833599000, startTime=1517414400000, account=None):
        '''会员快速查询'''
        url = "http://" + self.host + self.auth.config.api["owner"]["search_member"]
        datas = {"end": endTime, "page": 1, "rows": 15, "start": startTime, "sideType": 2, "account": account}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【会员快速查询-request】" + str(datas))
        Pylog.info("【会员快速查询-resp】" + str(resp.text))
        return str(resp.text)

    def search_game(self, endTime=1519833599000, startTime=1517414400000, lotteryIds=2):
        '''游戏快速查询
            lotteryIds:
                2：重庆时时彩双面彩
        '''
        url = "http://" + self.host + self.auth.config.api["owner"]["search_game"]
        datas = {"end": endTime, "page": 1, "rows": 15, "start": startTime, "lotteryIds": lotteryIds}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【游戏快速查询-request】" + str(datas))
        Pylog.info("【游戏快速查询-resp】" + str(resp.text))
        return str(resp.text)

    def game_details(self, endTime=1519833599000, startTime=1517414400000, lotteryId=2, playId=21101):
        '''游戏玩法明细查看'''
        url = "http://" + self.host + self.auth.config.api["owner"]["game_details"]
        datas = {"end": endTime, "page": 1, "rows": 15, "start": startTime, "lotteryId": lotteryId, "playId": playId}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【游戏玩法明细查看-request】" + str(datas))
        Pylog.info("【游戏玩法明细查看-resp】" + str(resp.text))
        return str(resp.text)

    def statics_game(self, endPdate=1519833599000, startPdate=1517414400000, lotteryIds=2, source=2):
        '''游戏统计报表搜索
            source：
                2：H5
        '''
        url = "http://" + self.host + self.auth.config.api["owner"]["statics_game"]
        datas = {"endPdate": endPdate, "page": 1, "rows": 15, "startPdate": startPdate, "lotteryIds": lotteryIds, "source": source, "count": 15, "sideType": 2}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【游戏统计报表搜索-request】" + str(datas))
        Pylog.info("【游戏统计报表搜索-resp】" + str(resp.text))
        return str(resp.text)

    def statics_game_per_day(self, endPdate=1519833599000, startPdate=1517414400000, lotteryIds=2, source=2):
        '''单日游戏报表搜索
            source：
                2：H5
        '''
        url = "http://" + self.host + self.auth.config.api["owner"]["statics_game_per_day"]
        datas = {"endPdate": endPdate, "page": 1, "rows": 15, "startPdate": startPdate, "lotteryIds": lotteryIds, "source": source, "count": 15, "sideType": 2}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【单日游戏报表搜索-request】" + str(datas))
        Pylog.info("【单日游戏报表搜索-resp】" + str(resp.text))
        return str(resp.text)

    def statics_game_per_code(self, endPdate=1517500799000, startPdate=1517414400000, lotteryIds=2, source=2):
        '''单期游戏报表搜索
            source：
                2：H5
        '''
        url = "http://" + self.host + self.auth.config.api["owner"]["statics_game_per_code"]
        datas = {"endPdate": endPdate, "page": 1, "rows": 15, "startPdate": startPdate, "lotteryIds": lotteryIds, "source": source, "sideType": 2}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【单期游戏报表搜索-request】" + str(datas))
        Pylog.info("【单期游戏报表搜索-resp】" + str(resp.text))
        return str(resp.text)

    def gainlost_details(self, pCode=20180201002, pDate=20180201, lotteryId=2):
        '''玩法盈亏明细'''
        url = "http://" + self.host + self.auth.config.api["owner"]["gainlost_details"]
        datas = {"page": 1, "rows": 15, "lotteryId": lotteryId, "pCode": pCode, "pDate": pDate}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【玩法盈亏明细-request】" + str(datas))
        Pylog.info("【玩法盈亏明细-resp】" + str(resp.text))
        return str(resp.text)

    def backwater_stats(self, endTime=1519833599000, startTime=1517414400000):
        '''会员返水统计搜索'''
        url = "http://" + self.host + self.auth.config.api["owner"]["backwater_stats"]
        datas = {"page": 1, "rows": 15, "endTime": endTime, "startTime": startTime}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【会员返水统计搜索-request】" + str(datas))
        Pylog.info("【会员返水统计搜索-resp】" + str(resp.text))
        return str(resp.text)

    def member_backwater_stats(self, endTime=1519833599000, startTime=1517414400000, agentId=None):
        '''会员返水列表搜索'''
        url = "http://" + self.host + self.auth.config.api["owner"]["member_backwater_stats"]
        datas = {"page": 1, "rows": 15, "endTime": endTime, "startTime": startTime, "agentId": agentId}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【会员返水列表搜索-request】" + str(datas))
        Pylog.info("【会员返水列表搜索-resp】" + str(resp.text))
        return str(resp.text)

    def mem_cash_back_statistics_mem(self, endTime=1519833599000, startTime=1517414400000, agentId=None, memberAccount=None, memberId=None):
        '''会员返水详情查看'''
        url = "http://" + self.host + self.auth.config.api["owner"]["mem_cash_back_statistics_mem"]
        datas = {"agentId": agentId, "cashAgentAccount2": 'default', "endTime": endTime, "memberAccount": memberAccount, "memberId": memberId, "page": 1, "rows": 15, "startTime": startTime}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【会员返水详情查看-request】" + str(datas))
        Pylog.info("【会员返水详情查看-resp】" + str(resp.text))
        return str(resp.text)

    def r_com_stat_list(self, agentName='default', pcode=81):
        '''代理退佣统计搜索'''
        url = "http://" + self.host + self.auth.config.api["owner"]["r_com_stat_list"]
        datas = {"agentName": agentName, "page": 1, "pcode": pcode, "rows": 15}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【代理退佣统计搜索-request】" + str(datas))
        Pylog.info("【代理退佣统计搜索-resp】" + str(resp.text))
        return str(resp.text)

    def log_list(self, account=None, category=None, type=None):
        '''日志搜索
            type：
                6：登录
                7：登出
            category：
                2：代理日志
                默认：管理员日志
        '''
        url = "http://" + self.host + self.auth.config.api["owner"]["log_list"]
        datas = {"account": account, "category": 1, "page": 1, "rows": 15, "category": category, "type": type}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        if category == 2:
            Pylog.info("【代理日志搜索-resp】" + str(resp.text))
        else:
            Pylog.info("【管理员日志搜索-resp】" + str(resp.text))
        return str(resp.text)

    def agentPeriod_getSelectList(self, agentName='default', pcode=81):
        '''获取代理退佣期号'''
        url = "http://" + self.host + self.auth.config.api["owner"]["agentPeriod_getSelectList"]
        resp = requests.get(url=url, headers=self.headers)
        Pylog.info("【获取代理退佣期号-resp】" + str(resp.text))
        return str(resp.text)

if __name__ == "__main__":
    Pylog()
    #
    resp = Statics().mem_cash_back_statistics_mem()