# coding:utf-8
import requests
import json
import time

from utils import utils
from action.owner.uaa import Uaa
from utils.pylog import Pylog
from auth.authors import Authors
from config import globalvars


class ParamConfig():
    '''参数配置'''
    def __init__(self):
        self.config = globalvars.config()
        self.api = self.config.api
        owner = self.config.owner
        self.host = owner["env"]["host_yz"]
        self.headers = globalvars.get_value("headers_owner")
        self.headers["Origin"] = owner["env"]["origin_yz"]
        self.platId = owner["env"]["platId"]

    def user_list(self, account=None, roleId=None):
        '''账号管理搜索'''
        url = "http://" + self.host + self.config.api["owner"]["user_list"]
        datas = {"account": account, "page": 1, "roleId": roleId, "rows": 15}
        resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【账号管理搜索-request】" + str(datas))
        Pylog.debug("【账号管理搜索-resp】" + str(resp.text))
        return str(resp.text)

    def user_get(self, userId=125):
        '''修改账号时账号信息读取'''
        url = "http://" + self.host + self.config.api["owner"]["user_get"]
        datas = {"userId": userId}
        resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【修改账号时账号信息读取-request】" + str(datas))
        Pylog.debug("【修改账号时账号信息读取-resp】" + str(resp.text))
        return str(resp.text)

    def user_update(self, userId=125, nickName='test_len', roleId=400):
        '''修改账号'''
        url = "http://" + self.host + self.config.api["owner"]["user_update"]
        datas = {"nickName": nickName, "roleId": roleId, "userId": userId}
        resp = requests.post(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【修改账号-request】" + str(datas))
        Pylog.debug("【修改账号-resp】" + str(resp.text))
        return str(resp.text)

    def update_status(self, userId=125, status=1):
        '''停启用账号
            status：
                1：启用
                0：停用
        '''
        url = "http://" + self.host + self.config.api["owner"]["update_status"]
        datas = {"userId": userId, "status": status}
        resp = requests.post(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【停启用账号-request】" + str(datas))
        Pylog.debug("【停启用账号-resp】" + str(resp.text))
        return str(resp.text)

    def role_list(self):
        '''角色列表读取'''
        url = "http://" + self.host + self.config.api["owner"]["role_list"]
        datas = {"page": 1, "rows": 15}
        resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【角色列表读取-request】" + str(datas))
        Pylog.debug("【角色列表读取-resp】" + str(resp.text))
        return str(resp.text)

    def role_get(self, roleId=539):
        '''修改角色时角色信息读取'''
        url = "http://" + self.host + self.config.api["owner"]["role_get"]
        datas = {"roleId": roleId}
        resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【修改角色时角色信息读取-request】" + str(datas))
        Pylog.debug("【修改角色时角色信息读取-resp】" + str(resp.text))
        return str(resp.text)

    def role_update(self, roleName=None, description=None, resIds=None, roleId=None):
        '''修改角色'''
        url = "http://" + self.host + self.config.api["owner"]["role_update"]
        datas = {"roleName": roleName, "description": description, "resIds": resIds, "roleId": roleId}
        resp = requests.post(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【修改角色-request】" + str(datas))
        Pylog.debug("【修改角色-resp】" + str(resp.text))
        return str(resp.text)

    def registerConfig_list(self, regType=1):
        '''会员注册配置读取
            regType：
                1：会员
                2：代理
        '''
        try:
            url = "http://" + self.host + self.api["owner"]["registerConfig_list"]
            datas = {"regType": regType}
            resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
            if regType == 1:
                Pylog.debug("【会员注册配置读取-resp】" + str(resp.text))
            elif regType == 2:
                Pylog.debug("【代理注册配置读取-resp】" + str(resp.text))
            datas = json.loads(resp.text)["data"]["rows"]
            return datas
        except Exception:
            Pylog.error("【注册配置读取错误】：" + Pylog.exinfo())
            return "注册配置读取错误"

    def registerConfig_save(self, param):
        '''会员注册配置保存'''
        try:
            url = "http://" + self.host + self.api["owner"]["registerConfig_save"]
            for i in param:
                i["ifCheck"] = 0
                i["ifView"] = 1
                i["ifRequired"] = 1
            Pylog.debug("【会员注册配置保存-request】" + str(param))
            resp = requests.post(url=url, headers=self.headers, data=json.dumps(param), timeout=15)
            Pylog.debug("【会员注册配置保存-resp】" + str(resp.text))
            for i in param:
                i.pop("version")
                i.pop("ifDel")
                i.pop("createUser")
                i.pop("createTime")
                i.pop("modifyUser")
                i.pop("modifyTime")
            globalvars.set_value("regconfig", param)
            return resp.text
        except Exception:
            Pylog.error("【会员注册配置保存错误】：" + Pylog.exinfo())
            return "会员注册配置保存错误"

    def lotteryWeight_list(self):
        '''彩种排序读取'''
        url = "http://" + self.host + self.config.api["owner"]["lotteryWeight_list"]
        datas = {"page": 1, "rows": 100, "sideType": 2}
        resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【彩种排序读取-resp】" + str(resp.text))
        return str(resp.text)

    def lotteryWeight_save(self, param):
        '''彩种排序保存'''
        url = "http://" + self.host + self.config.api["owner"]["lotteryWeight_save"]
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(param), timeout=15)
        Pylog.debug("【彩种排序保存-resp】" + str(resp.text))
        return str(resp.text)

    def soundConfig_list(self):
        '''站点语音提示列表读取'''
        url = "http://" + self.host + self.config.api["owner"]["soundConfig_list"]
        datas = {"page": 1, "rows": 100}
        resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【站点语音提示列表读取-request】" + str(datas))
        Pylog.debug("【站点语音提示列表读取-resp】" + str(resp.text))
        return str(resp.text)

    def soundConfig_save(self, cid=1, status=1):
        '''语音提示停启用
            status:
                0：停用
                1：启用
        '''
        url = "http://" + self.host + self.config.api["owner"]["soundConfig_save"]
        datas = {"cid": cid, "status": status}
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(datas), timeout=15)
        Pylog.debug("【语音提示停启用-request】" + str(datas))
        Pylog.debug("【语音提示停启用-resp】" + str(resp.text))
        return str(resp.text)

    def custConfig_view(self):
        '''客服链接读取'''
        url = "http://" + self.host + self.config.api["owner"]["custConfig_view"]
        resp = requests.get(url=url, headers=self.headers)
        Pylog.debug("【客服链接读取-resp】" + str(resp.text))
        return str(resp.text)

    def custConfig_save(self, param):
        '''客服链接修改'''
        url = "http://" + self.host + self.config.api["owner"]["custConfig_save"]
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(param), timeout=15)
        Pylog.debug("【客服链接修改-resp】" + str(resp.text))
        return str(resp.text)

    def appConfig_view(self):
        '''app下载地址读取'''
        url = "http://" + self.host + self.config.api["owner"]["appConfig_view"]
        resp = requests.get(url=url, headers=self.headers)
        Pylog.debug("【app下载地址读取-resp】" + str(resp.text))
        return str(resp.text)

    def appConfig_save(self, param):
        '''app下载链接修改'''
        url = "http://" + self.host + self.config.api["owner"]["appConfig_save"]
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(param), timeout=15)
        Pylog.debug("【app下载链接修改-request】" + str(param))
        Pylog.debug("【app下载链接修改-resp】" + str(resp.text))
        return str(resp.text)

    def whiteips_list(self):
        '''白名单列表读取'''
        url = "http://" + self.host + self.config.api["owner"]["whiteips_list"]
        datas = {"page": 1, "rows": 15}
        resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【白名单列表读取-resp】" + str(resp.text))
        return str(resp.text)

    def whiteips_edit(self, id=52, domain='www3.baidu.com', ip='192.168.0.252'):
        '''白名单修改'''
        url = "http://" + self.host + self.config.api["owner"]["whiteips_edit"]
        datas = {"id": id, "domain": domain, "ip": ip}
        resp = requests.post(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【白名单修改-request】" + str(datas))
        Pylog.debug("【白名单修改-resp】" + str(resp.text))
        return str(resp.text)

    def whiteips_updateStatus(self, id=52, status=1):
        '''白名单停启用
            status：
                1：启用
                2：停用
        '''
        url = "http://" + self.host + self.config.api["owner"]["whiteips_updateStatus"]
        datas = {"id": id, "status": status}
        resp = requests.post(url=url, headers=self.headers, params=datas, timeout=15)
        Pylog.debug("【白名单停启用-request】" + str(datas))
        Pylog.debug("【白名单停启用-resp】" + str(resp.text))
        return str(resp.text)

    def reg_sameIp(self, times, num, status):
        '''同IP注册限制'''
        try:
            url = "http://" + self.host + "/ares-config/apis/plat/ipRegisterLimit/save"
            datas = {"status": status, "maxLimit": num, "renewRate": times}
            Pylog.debug("【同IP注册限制-request】" + str(datas))
            resp = requests.post(url=url, headers=self.headers, data=json.dumps(datas), timeout=15)
            Pylog.debug("【同IP注册限制-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【同IP注册限制错误】：" + Pylog.exinfo())
            return "同IP注册限制错误"

    def domain_list(self, agentAccount=None, domain=None, type=None):
        '''域名列表读取'''
        try:
            url = "http://" + self.host + self.api["owner"]["domain_list"]
            if "http://" in domain:
                domain = domain.replace("http://", "")
            datas = {"page": 1, "rows": 15, "agentAccount": agentAccount, "domain": domain, "type": type}
            Pylog.debug("【域名列表读取-request】" + str(datas))
            resp = requests.get(url=url, headers=self.headers, params=datas, timeout=15)
            Pylog.debug("【域名列表读取-resp】" + str(resp.text))
            return str(resp.text)
        except Exception:
            Pylog.error("【域名列表读取错误】：" + Pylog.exinfo())
            return "域名列表读取错误"

    def domain_saveByBatch(self, type=1, domains='autotest'):
        '''新增域名'''
        url = "http://" + self.host + self.config.api["owner"]["domain_saveByBatch"]
        datas = {"type": type, "domains": domains}
        resp = requests.post(url=url, headers=self.headers, params=datas)
        Pylog.debug("【新增域名-request】" + str(datas))
        Pylog.debug("【新增域名-resp】" + str(resp.text))
        return str(resp.text)

    def domain_save(self, param):
        '''域名停启用'''
        url = "http://" + self.host + self.config.api["owner"]["domain_save"]
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(param))
        Pylog.debug("【域名停启用-request】" + str(param))
        Pylog.debug("【域名停启用-resp】" + str(resp.text))
        return str(resp.text)

    def receipt_list(self):
        '''收款配置列表读取'''
        url = "http://" + self.host + self.config.api["owner"]["receipt_list"]
        resp = requests.get(url=url, headers=self.headers)
        Pylog.debug("【收款配置列表读取-resp】" + str(resp.text))
        return resp.text

    def receipt_edit(self, rsName='eee', rsUrl='http://wfsfsfsfs.s.s2', id=140):
        '''修改收款配置'''
        url = "http://" + self.host + self.config.api["owner"]["receipt_edit"]
        datas = {"rsName": rsName, "rsUrl": rsUrl, "id": id}
        resp = requests.post(url=url, headers=self.headers, params=datas)
        Pylog.debug("【修改收款配置-request】" + str(datas))
        Pylog.debug("【修改收款配置-resp】" + str(resp.text))
        return str(resp.text)

    def receipt_statusAll(self):
        '''快捷支付全部停启用'''
        try:
            clist = self.receipt_list()
            clist = json.loads(clist)["data"]
            for cid in clist:
                if cid["rsNameId"] == 0:
                    self.receipt_editstatus(cid=cid["id"], status=1)
            return "SUCCESS"
        except Exception:
            Pylog.error("【快捷支付全部停启用错误】：" + Pylog.exinfo())
            return "快捷支付全部停启用错误"

    def receipt_deleteAll(self):
        '''快捷支付全部删除'''
        try:
            url = "http://" + self.host + "/arespayment/apis/plat/receipt/delete"
            clist = self.receipt_list()
            clist = json.loads(clist)["data"]
            for cid in clist:
                if cid["rsNameId"] == 0:
                    requests.get(url=url, headers=self.headers, params={"cid": cid["id"]})
            return "SUCCESS"
        except Exception:
            Pylog.error("【快捷支付全部删除错误】：" + Pylog.exinfo())
            return "快捷支付全部删除错误"

    def receipt_create(self, rsName, raUrl):
        '''新增快捷支付'''
        try:
            url = "http://" + self.host + "/arespayment/apis/plat/receipt/add"
            datas = {"rsName": rsName, "rsUrl": raUrl, "sort": 50}
            resp = requests.post(url=url, headers=self.headers, params=datas)
            Pylog.debug("【新增快捷支付-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error("【新增快捷支付错误】：" + Pylog.exinfo())
            return "新增快捷支付错误"

    def receipt_editstatus(self, flag=1, cid=140, status=0):
        '''收款配置停启用'''
        try:
            url = "http://" + self.host + self.config.api["owner"]["receipt_editstatus"]
            datas = {"flag": flag, "id": cid, "status": status}
            resp = requests.get(url=url, headers=self.headers, params=datas)
            Pylog.debug("【收款配置停启用-resp】" + str(resp.text))
            return str(resp.text)
        except Exception:
            Pylog.error("【收款配置停启用错误】：" + Pylog.exinfo())
            return "收款配置停启用错误"

    def income_list(self):
        '''公司入款账号搜索
            status:
                -1：全部
                0：停用
        '''
        try:
            url = "http://" + self.host + self.api["owner"]["income_list"]
            datas = {"page": 1, "rows": 15}
            Pylog.debug("【公司入款账号搜索-request】" + str(datas))
            resp = requests.get(url=url, headers=self.headers, params=datas)
            Pylog.debug("【公司入款账号搜索-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【公司入款账号搜索错误】：" + Pylog.exinfo())
            return "公司入款账号搜索错误"

    def memberLevel_getSelectList(self):
        '''会员层级列表获取'''
        url = "http://" + self.host + self.api["owner"]["memberLevel_getSelectList"]
        resp = requests.get(url=url, headers=self.headers)
        Pylog.debug("【会员层级列表获取-resp】" + str(resp.text))
        return resp.text

    def income_create(self, level):
        '''新增公司入款方式'''
        try:
            url = "http://" + self.host + self.api["owner"]["income_create"]
            # levels = json.loads(self.memberLevel_getSelectList())["data"]
            random_income = str(time.time()).replace(".", "")
            datas = {
                "currency": "CNY",
                "cardOwnerName": "自动化收款人",
                "bankCode": "CCB",
                "bankName": "建设银行",
                "cardNo": random_income,
                "registerBankInfo": "自动化开户行",
                "stopAmount": 888800,
                "warnAmount": 88800,
                "transferRemark": None,
                "userLevels": [level]}
            Pylog.debug("【新增公司入款方式-request】" + str(datas))
            resp = requests.post(url=url, data=json.dumps(datas), headers=self.headers)
            Pylog.debug("【新增公司入款方式-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error("【新增公司入款错误】：" + Pylog.exinfo())
            return "新增公司入款错误"

    def income_edit(self, cid):
        '''公司入款账号修改'''
        try:
            url = "http://" + self.host + self.api["owner"]["income_edit"]
            for i in json.loads(self.income_list())["data"]["rows"]:
                if str(i["id"]) == str(cid):
                    memberInfo = json.loads(Uaa().member_info(globalvars.get_value("membername")))["data"]
                    i["userLevels"] = [{"id": memberInfo["levelId"], "value": memberInfo["levelName"]}]
                    Pylog.debug("【公司入款账号修改-request】" + str(i))
                    resp = requests.post(url=url, headers=self.headers, data=json.dumps(i))
                    Pylog.debug("【公司入款账号修改-resp】" + str(resp.text))
                    return str(resp.text)
        except Exception:
            Pylog.error("【公司入款账号修改错误】：" + Pylog.exinfo())
            return "公司入款账号修改错误"

    def income_status(self, cid, status):
        '''公司入款账号停启用
            status：
                0：停用
                1：启用
        '''
        try:
            url = "http://" + self.host + self.api["owner"]["income_status"]
            datas = {"id": cid, "status": status}
            Pylog.debug("【公司入款账号停启用-request】" + str(datas))
            resp = requests.get(url=url, headers=self.headers, params=datas)
            Pylog.debug("【公司入款账号停启用-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【公司入款账号停启用错误】：" + Pylog.exinfo())
            return "公司入款账号停启用错误"

    def income_delete(self, cid):
        '''公司入款账号删除'''
        try:
            url = "http://" + self.host + "/arespayment/apis/plat/income/delete"
            self.income_status(cid=cid, status=0)
            resp = requests.get(url=url, headers=self.headers, params={"cid": cid})
            Pylog.debug("【公司入款账号删除-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【公司入款账号删除错误】：" + Pylog.exinfo())
            return "公司入款账号删除错误"

    def income_deleteAll(self):
        '''公司入款账号全部删除'''
        try:
            clist = self.income_list()
            clist = json.loads(clist)["data"]["rows"]
            for i in clist:
                self.income_delete(i["id"])
            return "SUCCESS"
        except Exception:
            Pylog.error("【出入款优惠方案删除全部错误】：" + Pylog.exinfo())
            return "出入款优惠方案删除全部错误"

    def thirdpay_list(self, merchantName=None, status=-1):
        '''第三方支付搜索'''
        try:
            url = "http://" + self.host + self.config.api["owner"]["thirdpay_list"]
            datas = {"count": 15, "page": 1, "status": status, "merchantName": merchantName}
            resp = requests.get(url=url, headers=self.headers, params=datas)
            Pylog.debug("【第三方支付搜索-resp】" + str(resp.text))
            return str(resp.text)
        except Exception:
            Pylog.error("【第三方支付搜索错误】：" + Pylog.exinfo())
            return "第三方支付搜索错误"

    def thirdpay_create(self, merchantName, accountNo, pwd):
        '''新增第三方支付'''
        try:
            url_list = "http://" + self.host + "/arespayment/apis/plat/thirdpay/payment/list"
            url_type = "http://" + self.host + "/arespayment/apis/plat/thirdpay/payment/type"
            url = "http://" + self.host + "/arespayment/apis/plat/thirdpay/add"
            clist = requests.get(url=url_list, headers=self.headers)
            Pylog.debug("【获取第三方-resp】" + clist.text)
            clist = json.loads(clist.text)["data"]
            for cid in clist:
                if cid["paymentName"] == merchantName:
                    paymentId = cid["paymentId"]
            types = requests.get(url=url_type, headers=self.headers, params={"paymentId": paymentId})
            types = json.loads(types.text)["data"]
            datas = {
                "currency": "CNY", "merchantName": merchantName, "merchantNo": accountNo, "paymentId": paymentId,
                "paymentTypeId": types["paymentTypeId"],
                "stopAmount": 9999900, "warnAmount": 8888800, "merchantKey": pwd,
                "merchantPublicKey": pwd,
                "thirdTerminalId": None, "merchantDomain": None,
                "userLevels": [globalvars.get_value("member_level")],
                "paymentTypeName": types["paymentName"],
                "paymentName": merchantName
            }
            Pylog.debug("【新增第三方支付-request】" + str(datas))
            resp = requests.post(url=url, headers=self.headers, data=json.dumps(datas))
            Pylog.debug("【新增第三方支付-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error("【新增第三方支付错误】：" + Pylog.exinfo())
            return "新增第三方支付错误"

    def thirdpay_delete(self, merchantName):
        '''第三方支付删除'''
        try:
            url = "http://" + self.host + "/arespayment/apis/plat/thirdpay/delete"
            clist = self.thirdpay_list(merchantName=merchantName)
            clist = json.loads(clist)["data"]["rows"]
            if len(clist) == 0:
                return "SUCCESS"
            else:
                for cid in clist:
                    cid = cid["id"]
                    self.thirdpay_status(cid=cid, status=0)
                    resp = requests.get(url=url, headers=self.headers, params={"cid": cid})
                    Pylog.debug("【第三方支付删除-resp】" + str(resp.text))
                return "SUCCESS"
        except Exception:
            Pylog.error("【第三方支付删除错误】：" + Pylog.exinfo())
            return "第三方支付删除错误"

    def thirdpay_edit(self, param=None):
        '''第三方支付修改'''
        url = "http://" + self.host + self.config.api["owner"]["thirdpay_edit"]
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(param))
        Pylog.debug("【第三方支付修改-request】" + str(param))
        Pylog.debug("【第三方支付修改-resp】" + str(resp.text))
        return str(resp.text)

    def thirdpay_statusAll(self, status):
        '''第三方支付全部停启用'''
        try:
            clist = self.thirdpay_list(status=1)
            clist = json.loads(clist)["data"]["rows"]
            for cid in clist:
                self.thirdpay_status(cid=cid["id"], status=status)
            return "SUCCESS"
        except Exception:
            Pylog.error("【第三方支付全部停启用错误】：" + Pylog.exinfo())
            return "第三方支付全部停启用错误"

    def thirdpay_status(self, cid, status=0):
        '''第三方支付停启用
            status：
                0：停用
                1：启用
        '''
        try:
            url = "http://" + self.host + self.config.api["owner"]["thirdpay_status"]
            datas = {"id": cid, "status": status}
            resp = requests.get(url=url, headers=self.headers, params=datas)
            Pylog.debug("【第三方支付停启用-resp】" + str(resp.text))
            return str(resp.text)
        except Exception:
            Pylog.error("【第三方支付停启用错误】：" + Pylog.exinfo())
            return "第三方支付停启用错误"

    def registDiscount_list(self, name=None):
        '''注册优惠搜索'''
        try:
            url = "http://" + self.host + self.api["owner"]["registDiscount_list"]
            datas = {"name": name, "page": 1, "rows": 15}
            resp = requests.get(url=url, headers=self.headers, params=datas)
            Pylog.debug("【注册优惠搜索-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【注册优惠搜索错误】：" + Pylog.exinfo())
            return "注册优惠搜索错误"

    def registDiscount_delete(self, ids):
        '''注册优惠删除'''
        try:
            url = "http://" + self.host + "/ares-config/apis/plat/registDiscount/onStatus"
            url_d = "http://" + self.host + "/ares-config/apis/plat/registDiscount/delete"
            resp = requests.get(url=url, headers=self.headers, params={"id": ids, "status": 0})
            Pylog.debug("【注册优惠停用-resp】" + str(resp.text))

            resp = requests.get(url=url_d, headers=self.headers, params={"cid": ids})
            Pylog.debug("【注册优惠删除-resp】" + str(resp.text))

            return resp.text
        except Exception:
            Pylog.error("【注册优惠删除错误】：" + Pylog.exinfo())
            return "注册优惠删除用错误"

    def registDiscount_deleteAll(self):
        '''注册优惠全部删除'''
        clist = self.registDiscount_list()
        clist = json.loads(clist)["data"]["rows"]
        for i in clist:
            self.registDiscount_delete(i["cid"])
        return "SUCCESS"

    def registDiscount_create(self, name, money, audit):
        '''新增注册优惠方案'''
        try:
            url = "http://" + self.host + "/ares-config/apis/plat/registDiscount/save"
            datas = {"name": name, "discountedPrice": 100 * money, "auditMultiple": audit}
            resplist = self.registDiscount_list(name)
            if len(json.loads(resplist)["data"]["rows"]) == 1:
                cid = json.loads(resplist)["data"]["rows"][0]["cid"]
                return int(cid)
            Pylog.debug("【新增注册优惠方案-request】" + str(datas))
            resp = requests.post(url=url, headers=self.headers, data=json.dumps(datas))
            Pylog.debug("【新增注册优惠方案-resp】" + str(resp.text))
            cid = json.loads(resp.text)["data"]
            return int(cid)
        except Exception:
            Pylog.error("【新增注册优惠方案错误】：" + Pylog.exinfo())
            return "新增注册优惠方案错误"

    def registDiscount_onStatus(self, id=104, status=0):
        '''注册优惠方案停启用
            status：
                0：停用
                1：启用
        '''
        url = "http://" + self.host + self.api["owner"]["registDiscount_onStatus"]
        datas = {"id": id, "status": status}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【注册优惠方案停启用停启用-request】" + str(datas))
        Pylog.debug("【注册优惠方案停启用停启用-resp】" + str(resp.text))
        return str(resp.text)

    def retirement_list(self, name='leo'):
        '''代理退佣方案搜索'''
        url = "http://" + self.host + self.config.api["owner"]["retirement_list"]
        datas = {"name": name, "page": 1, "rows": 15}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【代理退佣方案搜索-request】" + str(datas))
        Pylog.debug("【代理退佣方案搜索-resp】" + str(resp.text))
        return str(resp.text)

    def retirement_save(self, param=None):
        '''代理退佣方案修改'''
        url = "http://" + self.host + self.config.api["owner"]["retirement_save"]
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(param))
        Pylog.debug("【代理退佣方案修改-request】" + str(param))
        Pylog.debug("【代理退佣方案修改-resp】" + str(resp.text))
        return str(resp.text)

    def administrative_list(self, name='leo'):
        '''行政成本搜索'''
        url = "http://" + self.host + self.config.api["owner"]["administrative_list"]
        datas = {"name": name, "page": 1, "rows": 15}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【行政成本搜索-request】" + str(datas))
        Pylog.debug("【行政成本搜索-resp】" + str(resp.text))
        return str(resp.text)

    def administrative_save(self, cid=27, percentage=100, name="leo"):
        '''行政成本修改'''
        url = "http://" + self.host + self.config.api["owner"]["administrative_save"]
        datas = {"cid": cid, "percentage": percentage, "name": name}
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(datas))
        Pylog.debug("【行政成本修改-request】" + str(datas))
        Pylog.debug("【行政成本修改-resp】" + str(resp.text))
        return str(resp.text)

    def administrative_onStatus(self, id=27, status=0):
        '''行政成本停启用'''
        url = "http://" + self.host + self.config.api["owner"]["administrative_onStatus"]
        datas = {"id": id, "status": status}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【行政成本停启用-request】" + str(datas))
        Pylog.debug("【行政成本停启用-resp】" + str(resp.text))
        return str(resp.text)

    def feePlan_list(self, name='leo'):
        '''手续费方案搜索'''
        url = "http://" + self.host + self.config.api["owner"]["feePlan_list"]
        datas = {"name": name, "page": 1, "rows": 15}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【手续费方案搜索-request】" + str(datas))
        Pylog.debug("【手续费方案搜索-resp】" + str(resp.text))
        return str(resp.text)

    def feePlan_save(self, cid=14, name="leo", depositFeePer=231, depositFeeLimit=100, withdrawalFeePer=100,
                     withdrawalFeeLimit=100):
        '''手续费方案修改'''
        url = "http://" + self.host + self.config.api["owner"]["feePlan_save"]
        datas = {"cid": cid, "depositFeePer": depositFeePer, "name": name, "depositFeeLimit": depositFeeLimit,
                 "withdrawalFeePer": withdrawalFeePer, "withdrawalFeeLimit": withdrawalFeeLimit}
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(datas))
        Pylog.debug("【手续费方案修改-request】" + str(datas))
        Pylog.debug("【手续费方案修改-resp】" + str(resp.text))
        return str(resp.text)

    def feePlan_onStatus(self, id=14, status=0):
        '''手续费方案停启用'''
        url = "http://" + self.host + self.config.api["owner"]["feePlan_onStatus"]
        datas = {"id": id, "status": status}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【手续费方案停启用-request】" + str(datas))
        Pylog.debug("【手续费方案停启用-resp】" + str(resp.text))
        return str(resp.text)

    def rebateProgram_list(self, name='leo'):
        '''会员返水方案搜索'''
        url = "http://" + self.host + self.config.api["owner"]["rebateProgram_list"]
        datas = {"name": name, "page": 1, "rows": 15}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【会员返水方案搜索-request】" + str(datas))
        Pylog.debug("【会员返水方案搜索-resp】" + str(resp.text))
        return str(resp.text)

    def rebateProgram_save(self, param=None):
        '''返水方案修改'''
        url = "http://" + self.host + self.config.api["owner"]["rebateProgram_save"]
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(param))
        Pylog.debug("【返水方案修改-request】" + str(param))
        Pylog.debug("【返水方案修改-resp】" + str(resp.text))
        return str(resp.text)

    def rebateProgram_onStatus(self, id=34, status=0):
        '''返水方案停启用'''
        url = "http://" + self.host + self.config.api["owner"]["rebateProgram_onStatus"]
        datas = {"id": id, "status": status}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【返水方案停启用-request】" + str(datas))
        Pylog.debug("【返水方案停启用-resp】" + str(resp.text))
        return str(resp.text)

    def accessDiscount_list(self, title=None):
        '''出入款方案搜索'''
        url = "http://" + self.host + self.api["owner"]["accessDiscount_list"]
        datas = {"page": 1, "rows": 15, "title": title}
        resp = requests.get(url=url, headers=self.headers, params=datas)
        Pylog.debug("【出入款方案搜索-resp】" + str(resp.text))
        return resp.text

    def accessDiscount_view(self, cid):
        '''出入款方案明细'''
        try:
            url = "http://" + self.host + self.api["owner"]["accessDiscount_view"]
            Pylog.debug("【出入款方案明细-request】" + str({"cid": cid}))
            resp = requests.get(url=url, headers=self.headers, params={"cid": cid})
            Pylog.debug("【出入款方案明细-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【出入款方案明细错误】：" + Pylog.exinfo())
            return "出入款方案明细错误"

    def accessDiscount_create(self, title):
        '''新增出入款方案'''
        try:
            url = "http://" + self.host + "/ares-config/apis/plat/accessDiscount/save"
            datasModel = self.config.model("owner", "accessDiscountCreate.json")
            datasModel["title"] = title
            Pylog.debug("【新增出入款方案-request】" + str(datasModel))
            resp = requests.post(url=url, headers=self.headers, data=json.dumps(datasModel))
            Pylog.debug("【新增出入款方案-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【新增出入款方案错误】：" + Pylog.exinfo())
            return "新增出入款方案错误"

    def accessDiscount_save(self, cid):
        '''保存出入款优惠设定'''
        try:
            url = "http://" + self.host + self.api["owner"]["accessDiscount_save"]
            datasModel = self.config.model("owner", "accessDiscount.json")
            datas = json.loads(self.accessDiscount_view(cid))["data"]
            datas["dispFee"] = datasModel["dispFee"]
            datas["dispFeeLimit"] = datasModel["dispFeeLimit"]
            datas["dispCapped"] = datasModel["dispCapped"]
            datas["dispLower"] = datasModel["dispLower"]
            datas["freeCount"] = datasModel["freeCount"]
            datas["repeatFeeCount"] = datasModel["repeatFeeCount"]
            datas["dailyAmountLimit"] = datasModel["dailyAmountLimit"]
            datas.pop("version"), datas.pop("ifDel"), datas.pop("createUser"), datas.pop("createTime")
            datas.pop("modifyUser"), datas.pop("modifyTime"), datas.pop("platId"), datas.pop("status")
            datas.pop("modifyUsername"), datas.pop("canModify")
            for i in range(0, 5):
                datas["itemPO"][i]["depositType"] = datasModel["itemPO"][i]["depositType"]
                datas["itemPO"][i]["ifFirst"] = datasModel["itemPO"][i]["ifFirst"]
                datas["itemPO"][i]["preferentialStandards"] = datasModel["itemPO"][i]["preferentialStandards"]
                datas["itemPO"][i]["discountPercentage"] = datasModel["itemPO"][i]["discountPercentage"]
                datas["itemPO"][i]["maxDepositAmount"] = datasModel["itemPO"][i]["maxDepositAmount"]
                datas["itemPO"][i]["minDepositAmount"] = datasModel["itemPO"][i]["minDepositAmount"]
                datas["itemPO"][i]["discountAudit"] = datasModel["itemPO"][i]["discountAudit"]
                datas["itemPO"][i]["ifNormalAudit"] = datasModel["itemPO"][i]["ifNormalAudit"]
                datas["itemPO"][i]["normalAuditQuota"] = datasModel["itemPO"][i]["normalAuditQuota"]
                datas["itemPO"][i]["normalAuditRate"] = datasModel["itemPO"][i]["normalAuditRate"]

            Pylog.debug("【保存出入款优惠设定-request】" + str(datas))
            resp = requests.post(url=url, headers=self.headers, data=json.dumps(datas))
            Pylog.debug("【保存出入款优惠设定-resp】" + str(resp.text))
            return str(resp.text)
        except Exception:
            Pylog.error("【保存出入款优惠设定错误】：" + Pylog.exinfo())
            return "保存出入款优惠设定错误"

    def accessDiscount_delete(self, ids):
        '''出入款优惠方案删除'''
        try:
            url = "http://" + self.host + self.api["owner"]["accessDiscount_onStatus"]
            url_d = "http://" + self.host + "/ares-config/apis/plat/accessDiscount/delete"
            resp = requests.get(url=url, headers=self.headers, params={"id": ids, "status": 0})
            Pylog.debug("【出入款优惠方案停用-resp】" + str(resp.text))

            resp = requests.get(url=url_d, headers=self.headers, params={"cid": ids})
            Pylog.debug("【出入款优惠方案删除-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【出入款优惠方案删除错误】：" + Pylog.exinfo())
            return "出入款优惠方案删除错误"

    def accessDiscount_deleteAll(self):
        '''出入款优惠方案删除全部'''
        try:
            clist = self.accessDiscount_list()
            clist = json.loads(clist)["data"]["rows"]
            for i in clist:
                self.accessDiscount_delete(i["cid"])
            return "SUCCESS"
        except Exception:
            Pylog.error("【出入款优惠方案删除全部错误】：" + Pylog.exinfo())
            return "出入款优惠方案删除全部错误"

    def registDiscount_save(self, name='autotest111', discountedPrice=100, auditMultiple=1):
        '''注册优惠设定'''
        url = "http://" + self.host + self.api["owner"]["registDiscount_save"]
        datas = {"name": name, "discountedPrice": discountedPrice, "auditMultiple": auditMultiple}
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(datas))
        Pylog.debug("【注册优惠设定-request】" + str(datas))
        Pylog.debug("【注册优惠设定-resp】" + str(resp.text))
        return str(resp.text)

    def walletpay_list(self, accountType=1):
        '''钱包支付列表'''
        try:
            url = "http://" + self.host + "/arespayment/apis/plat/walletpay/list"
            params = {"accountType": accountType, "page": 1, "pageSize": 15, "pageNo": 1}
            resp = requests.get(url=url, headers=self.headers, params=params)
            Pylog.debug("【钱包支付列表-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【获取钱包支付列表错误】：" + Pylog.exinfo())
            return "获取钱包支付列表错误"

    def walletpay_create(self, accountType):
        '''钱包支付新增'''
        try:
            paths = utils.findPath()
            userlevels = globalvars.get_value("member_level")
            types = "wx"
            if accountType == 2:
                types = "zfb"

            url = "http://" + self.host + "/arespayment/apis/plat/walletpay/add"
            url_up = "http://admin.baochiapi.com/photo/upload"
            file_up = {'pic': (open(paths + 'datas\\urlcode.png', 'rb'), 'image/png')}
            self.headers["Content-Type"] = None
            self.headers["Accept"] = "*/*"
            picid = requests.post(url=url_up, files=file_up, headers=self.headers)
            picid = json.loads(picid.text)["picid"]
            self.headers["Content-Type"] = "application/json; charset=UTF-8"
            datas = {"currency": "CNY", "accountNo": "{}_zhanghao{}".format(types, self.platId),
                     "accountName": "{}_mingcheng".format(types),
                     "realName": "{}_xingming".format(types), "qrCode": picid, "accountType": accountType,
                     "showRealName": 1,
                     "showAccountNo": 1, "showAccountName": 1, "userLevels": [userlevels]}
            Pylog.debug("【钱包支付新增-request】" + str(datas))
            resp = requests.post(url=url, headers=self.headers, data=json.dumps(datas))
            Pylog.debug("【钱包支付新增-resp】" + resp.text)
            return resp.text
        except Exception:
            Pylog.error("【钱包支付新增错误】：" + Pylog.exinfo())
            return "钱包支付新增错误"

    def walletpay_status(self, cid, status):
        '''钱包支付停启用'''
        try:
            url = "http://" + self.host + "/arespayment/apis/plat/walletpay/editstatus"
            params = {"id": cid, "status": status}
            resp = requests.get(url=url, headers=self.headers, params=params)
            Pylog.debug("【钱包支付停启用-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【钱包支付停启用错误】：" + Pylog.exinfo())
            return "钱包支付停启用错误"

    def walletpay_statusAll(self, status):
        '''钱包支付停启用全部'''
        try:
            url = "http://" + self.host + "/arespayment/apis/plat/walletpay/editstatus"
            clist1 = self.walletpay_list(accountType=1)
            clist2 = self.walletpay_list(accountType=2)
            clist = json.loads(clist1)["data"]["rows"] + json.loads(clist2)["data"]["rows"]
            for cid in clist:
                cid = cid["id"]
                params = {"id": cid, "status": status}
                resp = requests.get(url=url, headers=self.headers, params=params)
                Pylog.debug("【钱包支付停启用全部-resp】" + str(resp.text))
            return "SUCCESS"
        except Exception:
            Pylog.error("【钱包支付停启用全部错误】：" + Pylog.exinfo())
            return "钱包支付停启用全部错误"

    def walletpay_delete(self, cid):
        '''钱包支付删除'''
        try:
            url = "http://" + self.host + "/arespayment/apis/plat/walletpay/delete"
            params = {"cid": cid}
            resp = requests.get(url=url, headers=self.headers, params=params)
            Pylog.debug("【钱包支付删除-resp】" + str(resp.text))
            return resp.text
        except Exception:
            Pylog.error("【钱包支付删除错误】：" + Pylog.exinfo())
            return "钱包支付删除错误"

    def walletpay_deleteAll(self):
        '''钱包支付删除全部'''
        try:
            results1 = self.walletpay_list(accountType=1)
            results1 = json.loads(results1)["data"]["rows"]
            results2 = self.walletpay_list(accountType=2)
            results2 = json.loads(results2)["data"]["rows"]
            results = results1 + results2
            for i in results:
                self.walletpay_status(i["id"], 0)
                self.walletpay_delete(cid=i["id"])
            return "SUCCESS"
        except Exception:
            Pylog.error("【钱包支付删除全部错误】：" + Pylog.exinfo())
            return "钱包支付删除全部错误"


if __name__ == "__main__":
    Pylog()
    globalvars._init()
    Authors("owner")
    tmp = ParamConfig()
    # tmp.walletpay_deleteAll()
    tmp.thirdpay_create("高通支付QQ", 321654, "wertyui3456")
