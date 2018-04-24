# coding:utf-8
import requests
import json

from auth.authors import Authors
from utils.pylog import Pylog
from config import globalvars


class Uaa():
    '''账号管理'''
    def __init__(self, auth=None):
        self.config = globalvars.config()
        self.api = self.config.api
        owner = self.config.owner
        self.host = owner["env"]["host_mb"]
        self.headers = globalvars.get_value("headers_owner")
        self.headers["Origin"] = owner["env"]["origin_yz"]

    def memberList(self, name):
        '''会员列表获取'''
        try:
            url = "http://" + self.host + self.api["owner"]["memberList"]
            datas = {"login": name, "page": 1, "rows": 15}
            resp = requests.get(url=url, headers=self.headers, params=datas, timeout=5)
            Pylog.debug("【会员列表获取-resp】" + str(resp.text))
            return str(resp.text)
        except Exception:
            Pylog.error("【会员列表获取错误】：" + Pylog.exinfo())
            return "会员列表获取错误"

    def memberInfo(self, username="vctscript"):
        '''会员详情'''
        url = "http://" + self.host + self.api["owner"]["memberInfo"]
        datas = {"username": username}
        resp = requests.get(url=url, headers=self.headers, params=datas, timeout=5)
        Pylog.debug("【会员详情-request】" + str(datas))
        Pylog.info("【会员详情-resp】" + str(resp.text))
        return str(resp.text)

    def memberLevel(self):
        '''会员层级管理'''
        url = "http://" + self.host + self.api["owner"]["memberLevel_list"]
        datas = {"name": "", "page": 1, "rows": 15}
        resp = requests.get(url=url, params=datas, headers=self.headers, timeout=5)
        Pylog.debug("【会员层级管理-request】" + str(datas))
        Pylog.info("【会员层级管理-resp】" + str(resp.text))
        return str(resp.text)

    def agent_list(self, agentname=None):
        '''代理搜索'''
        try:
            url = "http://" + self.host + self.api["owner"]["agent_list"]
            datas = {"auditStatus": 1, "agentAccount": agentname, "page": 1, "rows": 15}
            Pylog.debug("【代理搜索-request】" + str(datas))
            resp = requests.get(url=url, params=datas, headers=self.headers)
            Pylog.debug("【代理搜索-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【代理搜索错误】：" + Pylog.exinfo())
            return "代理搜索错误"

    def agent_info(self, agentname=None):
        '''代理详情'''
        try:
            url = "http://" + self.host + "/areaaccount/apis/plat/agent/info"
            resp = requests.get(url=url, params={"username": agentname}, headers=self.headers)
            Pylog.debug("【代理详情-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【代理详情错误】：" + Pylog.exinfo())
            return "代理详情错误"

    def agent_save(self, agentAccount, memberLevelId=661, retirementId=29, administrativeId=27, feePlanId=14,
                   registerDiscountId=148):
        '''新增代理'''
        url = "http://" + self.host + self.api["owner"]["agent_save"]
        datas = {"isAudit": 0, "memberLevelId": memberLevelId, "retirementId": retirementId,
                 "administrativeId": administrativeId, "feePlanId": feePlanId, "registerDiscountId": registerDiscountId,
                 "preferentialCost": 0,
                 "rebateCost": 0, "domains": [], "agentAccount": agentAccount, "loginPwd": "123456", "agentName": "测试",
                 "bankNo": "6221003811111111", "bank": "测试",
                 "phone": "15211111111", "bankName": "工商银行"}
        resp = requests.post(url=url, data=json.dumps(datas), headers=self.headers)
        Pylog.debug("【新增代理-request】" + str(datas))
        Pylog.info("【新增代理-resp】" + str(resp.text))
        return str(resp.text)

    def agent_onStatus(self, cid, status):
        '''停启用代理账号
            status：
                1：启用
                0：停用
        '''
        url = "http://" + self.host + self.api["owner"]["agent_onStatus"]
        datas = {"cid": cid, "status": status}
        resp = requests.post(url=url, data=json.dumps(datas), headers=self.headers)
        Pylog.debug("【停启用代理账号-request】" + str(datas))
        Pylog.info("【停启用代理账号-resp】" + str(resp.text))
        return str(resp.text)

    def agent_listByAudit(self):
        '''待审核代理搜索'''
        url = "http://" + self.host + self.auth.config.api["owner"]["agent_listByAudit"]
        datas = {"auditStatus": 0, "isAudit": 1, "page": 1, "rows": 15}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.debug("【待审核代理搜索-request】" + str(datas))
        Pylog.info("【待审核代理搜索-resp】" + str(resp.text))
        return str(resp.text)

    def member_info(self, username):
        '''快速检测会员搜索'''
        try:
            url = "http://" + self.host + self.api["owner"]["member_info"]
            datas = {"username": username}
            resp = requests.get(url=url, params=datas, headers=self.headers)
            Pylog.debug("【快速检测会员搜索-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【快速检测会员搜索错误】：" + Pylog.exinfo())
            return "快速检测会员搜索"

    def member_chgInfo(self, memberId=None, email='5656@qq.com', wechat=234234, qq=234234, realName='测试'):
        '''修改会员信息'''
        url = "http://" + self.host + self.auth.config.api["owner"]["member_chgInfo"]
        datas = {"memberId": memberId, "email": email, "wechat": wechat, "qq": qq, "realName": realName}
        resp = requests.post(url=url, params=datas, headers=self.headers)
        Pylog.debug("【修改会员信息-request】" + str(datas))
        Pylog.info("【修改会员信息-resp】" + str(resp.text))
        return str(resp.text)

    def bank_update(self, memberId=None, bankCard="000000", bankAddress="测试地址", realName="第一次", bankName="农业银行"):
        '''修改会员银行信息'''
        url = "http://" + self.host + self.auth.config.api["owner"]["bank_update"]
        datas = {"bankCard": bankCard, "memberId": memberId, "bankAddress": bankAddress, "realName": realName,
                 "bankName": bankName}
        resp = requests.put(url=url, data=json.dumps(datas), headers=self.headers)
        Pylog.debug("【修改会员银行信息-request】" + str(datas))
        Pylog.info("【修改会员银行信息-resp】" + str(resp.text))
        return str(resp.text)

    def member_statusChange(self, memberID=4180, status=1):
        '''冻结解冻账号
            status：
                1：解冻
                0：冻结
        '''
        url = "http://" + self.host + self.auth.config.api["owner"]["member_statusChange"] + "/" + str(
            memberID) + "/" + str(status)
        resp = requests.get(url=url, headers=self.headers)
        if status == 1:
            Pylog.info("【解冻账号-resp】" + str(resp.text))
        if status == 0:
            Pylog.info("【冻结账号-resp】" + str(resp.text))
        return str(resp.text)

    def member_offline(self, username='bellajh1'):
        '''强制下线'''
        url = "http://" + self.host + self.auth.config.api["owner"]["member_offline"]
        datas = {"username": username}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.info("【强制下线-resp】" + str(resp.text))
        return str(resp.text)

    def member_password(self, memberId=4180, newPassword=123456):
        '''重置登录密码'''
        url = "http://" + self.host + self.auth.config.api["owner"]["member_password"]
        datas = {"memberId": memberId, "newPassword": newPassword}
        resp = requests.post(url=url, params=datas, headers=self.headers)
        Pylog.debug("【重置登录密码-request】" + str(datas))
        Pylog.info("【重置登录密码-resp】" + str(resp.text))
        return str(resp.text)

    def plat_update(self, memberId=4180, tradePassword=1234):
        '''重置取款密码'''
        url = "http://" + self.host + self.auth.config.api["owner"]["plat_update"]
        datas = {"memberId": memberId, "tradePassword": tradePassword}
        resp = requests.post(url=url, data=json.dumps(datas), headers=self.headers)
        Pylog.debug("【重置取款密码-request】" + str(datas))
        Pylog.info("【重置取款密码-resp】" + str(resp.text))
        return str(resp.text)

    def member_levelChange(self, memberID=99450, memberLevelId=478):
        '''更改层级'''
        url = "http://" + self.host + self.auth.config.api["owner"]["member_levelChange"] + "/" + str(
            memberID) + "/" + str(memberLevelId)
        resp = requests.get(url=url, headers=self.headers)
        Pylog.info("【更改层级-resp】" + str(resp.text))
        return str(resp.text)

    def agent_reset_pwd(self, agentId, pwd="123456"):
        '''重置代理登录密码'''
        url = "http://" + self.host + self.auth.config.api["owner"]["agent_reset_pwd"]
        datas = {"agentId": agentId, "newPassword": pwd, "password": pwd}
        resp = requests.post(url=url, params=datas, headers=self.headers)
        Pylog.debug("【重置代理登录密码-request】" + str(datas))
        Pylog.info("【重置代理登录密码-resp】" + str(resp.text))
        return str(resp.text)

    def agent_chgInfo(self, datas):
        '''修改代理信息'''
        try:
            url = "http://" + self.host + "/areaaccount/apis/plat/agent/chgInfo"
            Pylog.debug("【修改代理信息-request】" + str(datas))
            resp = requests.post(url=url, data=json.dumps(datas), headers=self.headers)
            Pylog.debug("【修改代理信息-resp】" + str(resp.text))
            return str(resp.text)
        except Exception:
            Pylog.error("【修改代理信息错误】：" + Pylog.exinfo())
            return "修改代理信息错误"

    def domain_listAgent(self):
        '''查看域名'''
        url = "http://" + self.host + self.auth.config.api["owner"]["domain_listAgent"]
        resp = requests.get(url=url, headers=self.headers)
        Pylog.info("【查看域名-resp】" + str(resp.text))
        return str(resp.text)

    def domain_updateDomainByAgent(self):
        '''绑定域名'''
        url = "http://" + self.host + self.auth.config.api["owner"]["domain_updateDomainByAgent"]
        datas = {"agnetId": 2364, "cids": [170, 182]}
        resp = requests.post(url=url, params=datas, headers=self.headers)
        Pylog.debug("【绑定域名-request】" + str(datas))
        Pylog.info("【绑定域名-resp】" + str(resp.text))
        return str(resp.text)

    def loglogin_list(self):
        '''同ip账号查询'''
        url = "http://" + self.host + self.auth.config.api["owner"]["loglogin_list"]
        datas = {"ip": '121.58.234.210', "loginType": 1, "page": 1, "rows": 15, "userName": 'justsoso'}
        resp = requests.get(url=url, params=datas, headers=self.headers)
        Pylog.debug("【同ip账号查询-request】" + str(datas))
        Pylog.info("【同ip账号查询-resp】" + str(resp.text))
        return str(resp.text)

    def memberLevel_save(self, accessDiscountId=456, rebateProgramId=0, name='test2'):
        '''新增会员层级'''
        url = "http://" + self.host + self.auth.config.api["owner"]["memberLevel_save"]
        datas = {"accessDiscountId": accessDiscountId, "rebateProgramId": rebateProgramId, "name": name}
        resp = requests.post(url=url, data=json.dumps(datas), headers=self.headers)
        Pylog.debug("【新增会员层级-request】" + str(datas))
        Pylog.info("【新增会员层级-resp】" + str(resp.text))
        return str(resp.text)

    def bank_view(self, memberId=1612488):
        '''会员银行详情'''
        url = "http://" + self.host + self.auth.config.api["owner"]["bank_view"]
        datas = {"memberId": memberId}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【会员银行详情-request】" + str(datas))
        Pylog.info("【会员银行详情-resp】" + str(resp.text))
        return str(resp.text)

    def level_list(self, levelName=None):
        '''层级搜索'''
        try:
            url = "http://" + self.host + "/uaa/apis/plat/memberLevel/list"
            resp = requests.get(url=url, headers=self.headers, params={"name": levelName, "page": 1, "rows": 15})
            Pylog.debug("【层级搜索-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【层级搜索错误】：" + Pylog.exinfo())
            return "层级搜索错误"

    def level_bind_acced(self, levelName, accessDiscountName, accessDiscountId):
        '''层级绑定优惠方案'''
        try:
            url = "http://" + self.host + "/uaa/apis/plat/memberLevel/save"
            datas = self.level_list(levelName)
            datas = json.loads(datas)["data"]["rows"][0]
            datas["accessDiscountName"] = accessDiscountName
            datas["accessDiscountId"] = accessDiscountId
            Pylog.debug("【层级绑定优惠方案-request】" + str(datas))
            resp = requests.post(url=url, headers=self.headers, data=json.dumps(datas))
            Pylog.debug("【层级绑定优惠方案-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【层级绑定优惠方案错误】：" + Pylog.exinfo())
            return "层级绑定优惠方案错误"

if __name__ == "__main__":
    Pylog()
    globalvars._init()
    Authors()
    Uaa().agent_info("leodl")
