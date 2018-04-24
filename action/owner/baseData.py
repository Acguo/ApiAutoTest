# coding:utf-8
import requests
import json
import time

from action.owner import content, paramConfig, payment, uaa
from action.owner.content import Content
from action.owner.paramConfig import ParamConfig
from action.owner.payment import Payment
from action.owner.statics import Statics
from action.owner.uaa import Uaa
from auth.authors import Authors
from pylog import Pylog


class BaseData():
    def __init__(self, auth=None):
        if auth == None:
            self.auth = Authors(types="owner")
        else:
            self.auth = auth
        self.host = self.auth.config.owner["env"]["host_yz"]
        self.headers = self.auth.headers

        self.content = Content(auth=self.auth)
        self.paramConfig = ParamConfig(auth=self.auth)
        self.payment = Payment(auth=self.auth)
        self.uaa = Uaa(auth=self.auth)
        self.statics = Statics(auth=self.auth)

        # 获取会员列表
        tmp = self.uaa.memberList()
        json_dict = json.loads(tmp)

        # 会员名字
        self.username = json_dict['rows'][0]['login']

        # 获取会员信息
        tmp = self.uaa.memberInfo(username=self.username)
        # 获取现有参数
        json_dict = json.loads(tmp)
        # 会员ID
        self.memberId = json_dict['data']['memberId']
        self.email = json_dict['data']['email']
        self.wechat = json_dict['data']['wechat']
        self.qq = json_dict['data']['qq']
        # 会员冻结状态
        self.memberStatus = json_dict['data']['status']
        # 获取已有的会员层级ID
        self.finalMemberLevelID = json_dict['data']['memberLevel']['cid']
        # 获取会员银行信息
        tmp = self.uaa.bank_view(memberId=self.memberId)
        json_dict = json.loads(tmp)
        self.bankCard = json_dict['data']['bankCard']
        self.bankAddress = json_dict['data']['bankAddress']
        self.realName = json_dict['data']['realName']
        self.bankName = json_dict['data']['bankName']

        # 获取retirementId
        self.name = "autoTest" + str(time.time())
        resp = self.paramConfig.retirement_save(param={"name":self.name,"effMemberNum":1,"currentEffBet":100,"currentProfit":100,"itemPO":[{"lotteryId":2,"percentage":0},{"lotteryId":4,"percentage":0},{"lotteryId":6,"percentage":0},{"lotteryId":8,"percentage":0},{"lotteryId":10,"percentage":0},{"lotteryId":12,"percentage":0},{"lotteryId":14,"percentage":0},{"lotteryId":16,"percentage":0},{"lotteryId":18,"percentage":0},{"lotteryId":20,"percentage":0},{"lotteryId":22,"percentage":0},{"lotteryId":24,"percentage":0},{"lotteryId":102,"percentage":0},{"lotteryId":104,"percentage":0},{"lotteryId":106,"percentage":0},{"lotteryId":108,"percentage":0},{"lotteryId":110,"percentage":0}]})
        respDict = json.loads(resp)
        self.retirementId = respDict['data']

        # 获取accessDiscountId
        self.name = "autoTest" + str(time.time())
        resp = self.paramConfig.accessDiscount_save(param={"title":self.name,"dispFee":100,"dispFeeLimit":100,"dispCapped":100,"dispLower":100,"freeCount":1,"repeatFeeCount":1,"dailyAmountLimit":1000000,"itemPO":[{"depositType":1,"ifFirst":1,"ifNormalAudit":1},{"depositType":1,"ifFirst":0,"ifNormalAudit":1},{"depositType":2,"ifFirst":1,"ifNormalAudit":1},{"depositType":2,"ifFirst":0,"ifNormalAudit":1},{"depositType":3,"ifFirst":0}]})
        respDict = json.loads(resp)
        self.accessDiscountId = respDict['data']

        # 获取新增的会员层级的memberLevelId
        self.name = "autoTest" + str(time.time())
        resp = self.uaa.memberLevel_save(accessDiscountId=self.accessDiscountId,rebateProgramId=0,name=self.name)
        respDict = json.loads(resp)
        self.memberLevelId = respDict['data']

        # 获取administrativeId
        self.name = "autoTest" + str(time.time())
        resp = self.paramConfig.administrative_save(cid=None,percentage=100,name=self.name)
        respDict = json.loads(resp)
        self.administrativeId = respDict['data']

        # 获取feePlanId
        self.name = "autoTest" + str(time.time())
        resp = self.paramConfig.feePlan_save(cid=None,name=self.name,depositFeePer=100,depositFeeLimit=100,withdrawalFeePer=100,withdrawalFeeLimit=100)
        respDict = json.loads(resp)
        self.feePlanId = respDict['data']

        # 获取registerDiscountId
        self.name = "autoTest" + str(time.time())
        resp = self.paramConfig.registDiscount_save(name=self.name,discountedPrice=100,auditMultiple=1)
        respDict = json.loads(resp)
        self.registerDiscountId = respDict['data']

        # 获取返水方案id
        # resp = self.payment.mem_cash_back_details(type=2, account=None)
        resp = self.paramConfig.rebateProgram_list(name=None)
        respDict = json.loads(resp)
        self.schemeId = respDict['data']['rows'][0]['cid']

        # 获取代理退佣期号ID
        resp = self.statics.agentPeriod_getSelectList()
        respDict = json.loads(resp)
        self.agentPeriodPcode = respDict['data'][0]['id']

        # 获取收款配置ID
        resp = self.paramConfig.receipt_list()
        respDict = json.loads(resp)
        self.receiptID = respDict['data'][0]['id']

        # 获取收款配置停启用状态
        self.receiptStatus = respDict['data'][0]['status']

        # 获取角色ID
        resp = self.paramConfig.role_list()
        respDict = json.loads(resp)
        self.roleId = respDict['data']['rows'][0]['roleId']

        # 获取角色名称
        resp = self.paramConfig.role_get(roleId=self.roleId)
        dictResp = json.loads(resp)
        self.roleName = dictResp['data']['name']

        # 获取角色描述
        resp = self.paramConfig.role_get(roleId=self.roleId)
        dictResp = json.loads(resp)
        self.roleDescription = dictResp['data']['description']

        # 获取开通的权限
        resp = self.paramConfig.role_get(roleId=self.roleId)
        dictResp = json.loads(resp)
        self.resIds = dictResp['data']['resIds']

        # 获取公司入款账号
        resp = self.paramConfig.income_list(status=None)
        dictResp = json.loads(resp)
        self.incomeID = dictResp['data']['rows'][0]['id']

        # 公司入款账号停启用状态
        self.incomeIdStatus = dictResp['data']['rows'][0]['status']

        # 获取有会员出款的会员名称
        resp = self.payment.draw_list(memberName=None, state=4)
        dictResp = json.loads(resp)
        self.memberNameForDraw = dictResp['data']['rows'][0]['memberName']

        # 获取有公司入款的卡号
        resp = self.payment.offline_statList(endTime= None, startTime= None)
        dictResp = json.loads(resp)
        self.cardNo = dictResp['data']['rows'][1]['cardNo']

        # 获取线上入款的商号和商家名称
        resp = self.payment.online_statList()
        dictResp = json.loads(resp)
        self.merchantNo = dictResp['data']['rows'][0]['merchantNo']
        self.merchantName = dictResp['data']['rows'][0]['merchantName']

        # 获取玩法盈亏pcode
        resp = self.statics.statics_game_per_code(endPdate=1517500799000, startPdate=1517414400000, lotteryIds=2, source=2)
        dictResp = json.loads(resp)
        self.gainlostPcode = dictResp['data']['rows'][0]['pcode']

        # 获取白名单ID
        resp = self.paramConfig.whiteips_list()
        dictResp = json.loads(resp)
        self.whiteipID = dictResp['data']['rows'][0]['id']
        # 获取白名单状态
        self.whiteipStatus = dictResp['data']['rows'][0]['status']
        # 获取白名单域名
        self.whiteipDomain = dictResp['data']['rows'][0]['domain']
        # 获取白名单ip
        self.whiteipIP = dictResp['data']['rows'][0]['ip']