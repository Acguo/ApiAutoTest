# coding:utf-8
import json
import unittest
import time

from action.memberaction import MemberAction
from action.owner.baseData import BaseData
from action.owner.content import Content
from action.owner.order import Order
from action.owner.ownerAction import OwnerAction
from action.owner.paramConfig import ParamConfig
from action.owner.payment import Payment
from action.owner.statics import Statics
from action.owner.statistics import Statistics
from action.owner.uaa import Uaa
from auth.authors import Authors
from pylog import Pylog
from config import configutil


class Ownercase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Pylog.info("***************开始执行用例（owner）***************")
        cls.auth = Authors(types="owner")
        cls.config = configutil.Config()

        cls.content = Content(auth=cls.auth)
        cls.order = Order(auth=cls.auth)
        cls.paramConfig = ParamConfig(auth=cls.auth)
        cls.payment = Payment(auth=cls.auth)
        cls.statics = Statics(auth=cls.auth)
        cls.statistics = Statistics(auth=cls.auth)
        cls.uaa = Uaa(auth=cls.auth)
        cls.baseData = BaseData(auth=cls.auth)

        cls.authMember= Authors(types="member")
        cls.ownerAction = OwnerAction(auth=cls.auth, authMember=cls.authMember)

    @classmethod
    def tearDownClass(cls):
        Pylog.info("***************结束执行用例（owner）***************")

    def test_001_今日方案(self):
        Pylog.info("【方案管理_方案记录_今日方案】")
        resp = self.order.order_todaylist()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_002_历史方案(self):
        Pylog.info("【方案管理_方案记录_历史方案】")
        resp = self.order.order_historylist()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_开奖历史(self):
        Pylog.info("【方案管理-开奖历史】")
        resp = self.order.prizeNumber()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_会员列表(self):
        Pylog.info("【账号管理-会员列表】")
        resp = self.uaa.memberList()
        dictResp = json.loads(resp)
        totalSize = dictResp['totalSize']
        self.assertGreater(totalSize, 0)

    def test_会员详情(self):
        Pylog.info("【账号管理-会员列表-会员详情】")
        resp = self.uaa.memberInfo()
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertIsNotNone(data)

    def test_会员层级管理(self):
        Pylog.info("【账号管理-会员层级管理】")
        resp = self.uaa.memberLevel()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_代理搜索(self):
        Pylog.info("【账号管理-代理列表-代理搜索】")
        resp = self.uaa.agent_list()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_代理新增_搜索_停启用_密码重置_修改信息(self):
        Pylog.info("【账号管理-代理列表-代理新增_搜索_停启用_密码重置_修改信息】")
        resp = self.ownerAction.agent(agentAccount=self.baseData.name, memberLevelId=self.baseData.memberLevelId, retirementId=self.baseData.retirementId, administrativeId=self.baseData.administrativeId, feePlanId=self.baseData.feePlanId, registerDiscountId=self.baseData.registerDiscountId)
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertGreater(data, 0)

    def test_待审核代理搜索(self):
        Pylog.info("【账号管理-新增代理审核-待审核代理搜索】")
        resp = self.uaa.agent_listByAudit()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_快速检测会员搜索(self):
        Pylog.info("【账号管理-快速检测-快速检测会员搜索】")
        resp = self.uaa.member_info()
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertIsNotNone(data)

    def test_修改会员信息(self):
        Pylog.info("【账号管理-快速检测-修改会员信息】")
        resp = self.uaa.member_chgInfo(memberId=self.baseData.memberId,email=self.baseData.email, wechat=self.baseData.wechat, qq=self.baseData.qq, realName=self.baseData.realName)
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertGreater(data, 0)

    def test_修改会员银行信息(self):
        Pylog.info("【账号管理-快速检测-修改会员银行信息】")
        resp = self.uaa.bank_update(memberId=self.baseData.memberId, bankCard=self.baseData.bankCard,bankAddress=self.baseData.bankAddress,realName=self.baseData.realName,bankName=self.baseData.bankName)
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_002_冻结解冻账号(self):
        Pylog.info("【账号管理-快速检测-冻结解冻账号】")
        resp = self.uaa.member_statusChange(memberID=self.baseData.memberId,status=self.baseData.memberStatus)
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertGreater(data, 0)

    def test_001_强制下线(self, userName='justsoso'):
        Pylog.info("【账号管理-快速检测-强制下线】")
        resp = self.ownerAction.member_offline(userName=userName)
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_重置登录密码(self):
        Pylog.info("【账号管理-快速检测-重置登录密码】")
        resp = self.uaa.member_password(memberId= self.baseData.memberId, newPassword= 123456)
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_重置取款密码(self):
        Pylog.info("【账号管理-快速检测-重置取款密码】")
        resp = self.uaa.plat_update(memberId= self.baseData.memberId, tradePassword= 1234)
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_更改层级(self):
        Pylog.info("【账号管理-快速检测-更改层级】")
        resp = self.uaa.member_levelChange(memberID=self.baseData.memberId, memberLevelId=self.baseData.finalMemberLevelID)
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertGreater(data, 0)

    def test_快速检测代理搜索(self):
        Pylog.info("【账号管理-快速检测-快速检测代理搜索】")
        resp = self.uaa.agent_info()
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertIsNotNone(data)

    def test_查看域名(self):
        Pylog.info("【账号管理-快速检测-查看域名】")
        resp = self.uaa.domain_listAgent()
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertIsNotNone(data)

    def test_绑定域名(self):
        Pylog.info("【账号管理-快速检测-绑定域名】")
        resp = self.uaa.domain_updateDomainByAgent()
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertGreater(data, 0)

    def test_同ip账号查询(self):
        Pylog.info("【账号管理-同ip账号查询】")
        resp = self.uaa.loglogin_list()
        dictResp = json.loads(resp)
        totalSize = dictResp['totalSize']
        self.assertGreater(totalSize, 0)

    def test_公司入款列表(self):
        Pylog.info("【资金管理-公司入款审核-公司入款列表】")
        resp = self.payment.chargeCmy_list()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_会员出款搜索_审核(self):
        Pylog.info("【资金管理-会员出款审核-会员出款搜索_审核】")
        resp = self.ownerAction.draw()
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertTrue(data)

    def test_出入款账目汇总查询(self):
        Pylog.info("【资金管理-出入款账目汇总-出入款账目汇总查询】")
        resp = self.payment.trade_statList()
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertIsNotNone(data)

    def test_出入款账目汇总_公司入款查询(self):
        Pylog.info("【资金管理-出入款账目汇总-出入款账目汇总_公司入款查询】")
        resp = self.payment.offline_statList()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_出入款账目汇总_公司入款详情查询(self):
        Pylog.info("【资金管理-出入款账目汇总-出入款账目汇总_公司入款详情查询】")
        resp = self.payment.offline_detail(endTime= None, startTime= None, cardNo= self.baseData.cardNo)
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_出入款账目汇总_线上入款查询(self):
        Pylog.info("【资金管理-出入款账目汇总-出入款账目汇总_线上入款查询】")
        resp = self.payment.online_statList()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_出入款账目汇总_线上入款详情查询(self):
        Pylog.info("【资金管理-出入款账目汇总-出入款账目汇总_线上入款详情查询】")
        resp = self.payment.online_detail(endTime= None, startTime= None, merchantNo= self.baseData.merchantNo, merchantName= self.baseData.merchantName)
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_出入款账目汇总_人工入款和会员出款扣款查询(self):
        Pylog.info("【资金管理-出入款账目汇总-出入款账目汇总_人工入款和会员出款扣款查询】")
        resp = self.payment.chargeanddraw_statList()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_出入款账目汇总_人工存款详情查询(self):
        Pylog.info("【资金管理-出入款账目汇总-出入款账目汇总_人工存款详情查询】")
        resp = self.payment.syscharge_detail()
        dictResp = json.loads(resp)
        totalSize = dictResp['totalSize']
        self.assertGreater(totalSize, 0)

    def test_出入款账目汇总_手续费扣除详情查询(self):
        Pylog.info("【资金管理-出入款账目汇总-出入款账目汇总_手续费扣除详情查询】")
        resp = self.payment.debit_detail()
        dictResp = json.loads(resp)
        totalSize = dictResp['totalSize']
        self.assertGreater(totalSize, 0)

    def test_出入款账目汇总_会员出款查询(self):
        Pylog.info("【资金管理-出入款账目汇总-出入款账目汇总_会员出款查询】")
        resp = self.payment.draw_statList()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_出入款账目汇总_会员出款详情查询(self):
        Pylog.info("【资金管理-出入款账目汇总-出入款账目汇总_会员出款详情查询】")
        resp = self.payment.draw_detail(endTime= None, startTime= None, memberName= self.baseData.memberNameForDraw)
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_出入款账目汇总_人工提出详情查询(self):
        Pylog.info("【资金管理-出入款账目汇总-出入款账目汇总_人工提出详情查询】")
        resp = self.payment.sysdraw_detail()
        dictResp = json.loads(resp)
        totalSize = dictResp['totalSize']
        self.assertGreater(totalSize, 0)

    def test_出入款账目汇总_给予返水查询(self):
        Pylog.info("【资金管理-出入款账目汇总-出入款账目汇总_给予返水查询】")
        resp = self.payment.cashback_statList()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_出入款账目汇总_给予返水详情查询(self):
        Pylog.info("【资金管理-出入款账目汇总-出入款账目汇总_给予返水详情查询】")
        resp = self.payment.backwater_detail()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_出入款账目汇总_给予优惠详情查询(self):
        Pylog.info("【资金管理-出入款账目汇总-出入款账目汇总_给予优惠详情查询】")
        resp = self.payment.discount_detail()
        dictResp = json.loads(resp)
        totalSize = dictResp['totalSize']
        self.assertGreater(totalSize, 0)

    def test_公司入款搜索_审核(self):
        Pylog.info("【资金管理-公司入款审核-公司入款搜索_审核】")
        resp = self.ownerAction.offline_charge()
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertTrue(data)

    def test_线上入款搜索_审核(self):
        Pylog.info("【资金管理-线上入款记录-线上入款搜索_审核】")
        resp = self.ownerAction.online_charge()
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertTrue(data)

    def test_即时稽核查询(self):
        Pylog.info("【资金管理-即时稽核查询】")
        resp = self.payment.member_audit()
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertIsNotNone(data)

    def test_人工存入账号信息查询(self):
        Pylog.info("【资金管理-人工存提-人工存入账号信息查询】")
        resp = self.payment.balance_get(memberName=self.baseData.username)
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertIsNotNone(data)

    def test_人工存入(self):
        Pylog.info("【资金管理-人工存提-人工存入】")
        resp = self.payment.system_charge(memberName=self.baseData.username, memberId=self.baseData.memberId)
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertTrue(data)

    def test_人工提出(self):
        Pylog.info("【资金管理-人工存提-人工提出】")
        resp = self.payment.system_draw(memberName=self.baseData.username, memberId=self.baseData.memberId)
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertTrue(data)

    def test_人工存入记录(self):
        Pylog.info("【资金管理-人工存入记录】")
        resp = self.payment.chargeanddraw_record(tradeType=5)
        dictResp = json.loads(resp)
        totalSize = dictResp['totalSize']
        self.assertGreater(totalSize, 0)

    def test_人工提出记录(self):
        Pylog.info("【资金管理-人工提出记录】")
        resp = self.payment.chargeanddraw_record(tradeType=8)
        dictResp = json.loads(resp)
        totalSize = dictResp['totalSize']
        self.assertGreater(totalSize, 0)

    def test_会员金流查询(self):
        Pylog.info("【资金管理-会员金流查询】")
        resp = self.payment.cashFlow_list()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_搜索会员返水列表(self):
        Pylog.info("【资金管理-会员返水管理-搜索会员返水列表】")
        resp = self.payment.mem_cash_back_details()
        dictResp = json.loads(resp)
        totalSize1 = dictResp['data']['totalSize']

        # 获取今日方案记录
        resp = self.order.order_todaylist()
        dictResp = json.loads(resp)
        totalSize2 = dictResp['data']['totalSize']

        if totalSize2 == 0:
            self.assertEqual(totalSize1, 0)
        else:
            self.assertGreater(totalSize1, 0)

    def test_查看返水方案(self):
        Pylog.info("【资金管理-会员返水管理-查看返水方案】")
        resp = self.payment.rebateProgram_view()
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertIsNotNone(data)

    def test_搜索退佣当期报表(self):
        Pylog.info("【资金管理-退佣当期报表-搜索退佣当期报表】")
        resp = self.payment.r_com_current_pcode_summary()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_查看退佣方案(self):
        Pylog.info("【资金管理-退佣当期报表-查看退佣方案】")
        resp = self.payment.retirement_view()
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertIsNotNone(data)

    def test_退佣账单详情(self):
        Pylog.info("【资金管理-退佣当期报表-退佣账单详情】")
        resp = self.payment.r_com_month_bill_detail()
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertIsNotNone(data)

    def test_出入款统计搜索(self):
        Pylog.info("【运营分析-出入款统计-出入款统计搜索】")
        resp = self.statistics.statistics_inout()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_会员入款明细(self):
        Pylog.info("【运营分析-出入款统计-会员入款明细】")
        resp = self.statistics.statistics_inList(memberName=None)
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_会员出款明细(self):
        Pylog.info("【运营分析-出入款统计-会员出款明细】")
        resp = self.statistics.statistics_outList()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_搜索会员优惠统计(self):
        Pylog.info("【运营分析-会员优惠统计-搜索会员优惠统计】")
        resp = self.statistics.discount_agent()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_查看会员优惠列表(self):
        Pylog.info("【运营分析-会员优惠统计-查看会员优惠列表】")
        resp = self.statistics.discount_member()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_查看会员优惠详情(self):
        Pylog.info("【运营分析-会员优惠统计-查看会员优惠详情】")
        resp = self.statistics.member_list(endTime=1519833599000, startTime=1517414400000, actionType=None, memberName=None)
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_查看会员返水记录(self):
        Pylog.info("【运营分析-会员返水记录-查看会员返水记录】")
        resp = self.statistics.mem_cash_back_record()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_查看会员扣款记录(self):
        Pylog.info("【运营分析-会员扣款记录-查看会员扣款记录】")
        resp = self.statistics.order_withhold()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_查看会员分层统计(self):
        Pylog.info("【运营分析-会员分层统计-查看会员分层统计】")
        resp = self.statistics.levelStatistics_list()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_查看会员注单统计(self):
        Pylog.info("【运营分析-会员注单统计-查看会员注单统计】")
        resp = self.statistics.levelStatistics_member_list(levelIds=None, lotteryIds=None)
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_搜索新增会员统计(self):
        Pylog.info("【运营分析-新增会员统计-搜索新增会员统计】")
        resp = self.statistics.statistics_memberDaylist()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_在线会员查询(self):
        Pylog.info("【运营分析-在线会员查询】")
        resp = self.statistics.online_list()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_代理统计报表搜索(self):
        Pylog.info("【统计查询-代理统计报表-代理统计报表搜索】")
        resp = self.statics.statics_agent()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_会员统计报表搜索(self):
        Pylog.info("【统计查询-代理统计报表-会员统计报表搜索】")
        resp = self.statics.statics_member()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_会员快速查询(self):
        Pylog.info("【统计查询-快速查询-会员快速查询】")
        resp = self.statics.search_member()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_游戏快速查询(self):
        Pylog.info("【统计查询-快速查询-游戏快速查询】")
        resp = self.statics.search_game()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_游戏玩法明细查看(self):
        Pylog.info("【统计查询-快速查询-游戏玩法明细查看】")
        resp = self.statics.game_details()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_游戏统计报表搜索(self):
        Pylog.info("【统计查询-游戏统计报表-游戏统计报表搜索】")
        resp = self.statics.statics_game()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_单日游戏报表搜索(self):
        Pylog.info("【统计查询-游戏统计报表-单日游戏报表搜索】")
        resp = self.statics.statics_game_per_day()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_单期游戏报表搜索(self):
        Pylog.info("【统计查询-游戏统计报表-单期游戏报表搜索】")
        resp = self.statics.statics_game_per_code()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_玩法盈亏明细(self):
        Pylog.info("【统计查询-游戏统计报表-玩法盈亏明细】")
        resp = self.statics.gainlost_details(pCode=self.baseData.gainlostPcode, pDate=None, lotteryId=2)
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_会员返水统计搜索(self):
        Pylog.info("【统计查询-会员返水统计-会员返水统计搜索】")
        resp = self.statics.backwater_stats()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_会员返水列表搜索(self):
        Pylog.info("【统计查询-会员返水统计-会员返水列表搜索】")
        resp = self.statics.member_backwater_stats()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_会员返水详情查看(self):
        Pylog.info("【统计查询-会员返水统计-会员返水详情查看】")
        resp = self.statics.mem_cash_back_statistics_mem()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_代理退佣统计搜索(self):
        Pylog.info("【统计查询-代理退佣统计-代理退佣统计搜索】")
        resp = self.statics.r_com_stat_list(pcode=self.baseData.agentPeriodPcode)
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_日志搜索(self):
        Pylog.info("【统计查询-日志查询与统计-日志搜索】")
        resp = self.statics.log_list()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)


    def test_账号管理搜索(self):
        Pylog.info("【参数配置-网站设定-权限管理-账号管理搜索】")
        resp = self.paramConfig.user_list()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_修改账号时账号信息读取(self):
        Pylog.info("【参数配置-网站设定-权限管理-修改账号时账号信息读取】")
        resp = self.paramConfig.user_get()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_修改业主账号(self):
        Pylog.info("【参数配置-网站设定-权限管理-修改业主账号】")
        resp = self.paramConfig.user_update()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_停启用业主账号(self):
        Pylog.info("【参数配置-网站设定-权限管理-停启用业主账号】")
        resp = self.paramConfig.update_status()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_角色管理搜索(self):
        Pylog.info("【参数配置-网站设定-权限管理-角色管理搜索】")
        resp = self.paramConfig.role_list()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_修改角色时角色信息读取(self):
        Pylog.info("【参数配置-网站设定-权限管理-修改角色时角色信息读取】")
        resp = self.paramConfig.role_get()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_修改角色(self):
        Pylog.info("【参数配置-网站设定-权限管理-修改角色】")
        resp = self.paramConfig.role_update(roleName=self.baseData.roleName, description=self.baseData.roleDescription, resIds=self.baseData.resIds, roleId=self.baseData.roleId)
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_会员注册配置读取(self):
        Pylog.info("【参数配置-网站设定-注册配置-会员注册配置读取】")
        resp = self.paramConfig.registerConfig_list()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_会员注册配置查询_更改(self):
        Pylog.info("【参数配置-网站设定-注册配置-会员注册配置查询_更改】")
        resp = self.ownerAction.registerConfig_member()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_代理注册配置查询_更改(self):
        Pylog.info("【参数配置-网站设定-注册配置-代理注册配置查询_更改】")
        resp = self.ownerAction.registerConfig_proxy()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_彩种排序读取(self):
        Pylog.info("【参数配置-网站设定-彩种排序-彩种排序读取】")
        resp = self.paramConfig.lotteryWeight_list()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_彩种排序权重读取_修改(self):
        Pylog.info("【参数配置-网站设定-彩种排序-彩种排序权重读取_修改】")
        resp = self.ownerAction.lotteryWeight()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_站点语音提示列表读取(self):
        Pylog.info("【参数配置-网站设定-站点语音提示-站点语音提示列表读取】")
        resp = self.paramConfig.soundConfig_list()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_语音提示读取_停启用(self):
        Pylog.info("【参数配置-网站设定-站点语音提示-语音提示读取_停启用】")
        resp = self.ownerAction.soundConfig()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_客服链接读取_修改(self):
        Pylog.info("【参数配置-网站设定-客服设定-客服链接读取_修改】")
        resp = self.ownerAction.custConfig()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_app下载链接读取_修改(self):
        Pylog.info("【参数配置-网站设定-APP地址设定-app下载链接读取_修改】")
        resp = self.ownerAction.appConfig()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_白名单列表读取(self):
        Pylog.info("【参数配置-网站设定-白名单设定-白名单列表读取】")
        resp = self.paramConfig.whiteips_list()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_白名单修改(self):
        Pylog.info("【参数配置-网站设定-白名单设定-白名单修改】")
        resp = self.paramConfig.whiteips_edit(id=self.baseData.whiteipID, domain=self.baseData.whiteipDomain, ip=self.baseData.whiteipIP)
        dictResp = json.loads(resp)
        try:
            err = dictResp['err']
        except KeyError:
            err = "FAIL"
        self.assertEqual("SUCCESS", err)

    def test_白名单停启用(self):
        Pylog.info("【参数配置-网站设定-白名单设定-白名单停启用】")
        resp = self.paramConfig.whiteips_updateStatus(id=self.baseData.whiteipID, status=self.baseData.whiteipStatus)
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_新增域名(self):
        Pylog.info("【参数配置-网站设定-域名列表-新增域名】")
        resp = self.paramConfig.domain_saveByBatch()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_域名信息读取_修改(self):
        Pylog.info("【参数配置-网站设定-域名列表-域名信息读取_修改】")
        resp = self.ownerAction.domain()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_收款配置列表读取(self):
        Pylog.info("【参数配置-收款方式-收款配置-收款配置列表读取】")
        resp = self.paramConfig.receipt_list()
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertIsNotNone(data)

    def test_修改收款配置(self):
        Pylog.info("【参数配置-收款方式-收款配置-修改收款配置】")
        resp = self.paramConfig.receipt_edit(id=self.baseData.receiptID)
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_收款配置停启用(self):
        Pylog.info("【参数配置-收款方式-收款配置-收款配置停启用】")
        resp = self.paramConfig.receipt_editstatus(id=self.baseData.receiptID, status=self.baseData.receiptStatus)
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_会员层级列表获取(self):
        Pylog.info("【参数配置-收款方式-公司入款账号设定-会员层级列表获取】")
        resp = self.paramConfig.memberLevel_getSelectList()
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertIsNotNone(data)

    def test_公司入款账号搜索_修改(self):
        Pylog.info("【参数配置-收款方式-公司入款账号设定-公司入款账号搜索_修改】")
        resp = self.ownerAction.income()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_公司入款账号停启用(self):
        Pylog.info("【参数配置-收款方式-公司入款账号设定-公司入款账号停启用】")
        if self.baseData.incomeIdStatus == 0:
            resp = self.paramConfig.income_status(id=self.baseData.incomeID, status=1)
        elif self.baseData.incomeIdStatus == 1:
            resp = self.paramConfig.income_status(id=self.baseData.incomeID, status=0)
        resp = self.paramConfig.income_status(id=self.baseData.incomeID, status=self.baseData.incomeIdStatus)
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_第三方支付搜索_修改(self):
        Pylog.info("【参数配置-收款方式-第三方支付设定-第三方支付搜索_修改】")
        resp = self.ownerAction.thirdpay()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_第三方支付停启用(self):
        Pylog.info("【参数配置-收款方式-第三方支付设定-第三方支付停启用】")
        resp = self.paramConfig.thirdpay_status()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_注册优惠搜索(self):
        Pylog.info("【参数配置-代理设定-注册优惠设定-注册优惠搜索】")
        resp = self.paramConfig.registDiscount_list(name=None)
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_注册优惠方案停启用(self):
        Pylog.info("【参数配置-代理设定-注册优惠设定-注册优惠方案停启用】")
        resp = self.paramConfig.registDiscount_onStatus()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_代理退佣方案搜索_修改(self):
        Pylog.info("【参数配置-代理设定-代理退佣设定-代理退佣方案搜索_修改】")
        resp = self.ownerAction.agent_retirement()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_行政成本搜索(self):
        Pylog.info("【参数配置-代理设定-行政成本设定-行政成本搜索】")
        resp = self.paramConfig.administrative_list()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_行政成本修改(self):
        Pylog.info("【参数配置-代理设定-行政成本设定-行政成本修改】")
        resp = self.paramConfig.administrative_save()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_行政成本停启用(self):
        Pylog.info("【参数配置-代理设定-行政成本设定-行政成本停启用】")
        resp = self.paramConfig.administrative_onStatus()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_手续费方案搜索(self):
        Pylog.info("【参数配置-代理设定-手续费设定-手续费方案搜索】")
        resp = self.paramConfig.feePlan_list()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_手续费方案修改(self):
        Pylog.info("【参数配置-代理设定-手续费设定-手续费方案修改】")
        resp = self.paramConfig.feePlan_save()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_手续费方案停启用(self):
        Pylog.info("【参数配置-代理设定-手续费设定-手续费方案停启用】")
        resp = self.paramConfig.feePlan_onStatus()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_会员返水方案查看_修改(self):
        Pylog.info("【参数配置-会员设定-会员返水设定-会员返水方案查看_修改】")
        resp = self.ownerAction.rebateProgram(cid=self.baseData.schemeId)
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_返水方案停启用(self):
        Pylog.info("【参数配置-会员设定-会员返水设定-返水方案停启用】")
        resp = self.paramConfig.rebateProgram_onStatus()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_出入款优惠方案查看_修改(self):
        Pylog.info("【参数配置-会员设定-出入款优惠设定-出入款优惠方案查看_修改】")
        resp = self.ownerAction.accessDiscount()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_出入款优惠方案停启用(self):
        Pylog.info("【参数配置-会员设定-出入款优惠设定-出入款优惠方案停启用】")
        resp = self.paramConfig.accessDiscount_onStatus()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_站点信息(self):
        Pylog.info("【内容管理-网站信息管理-站点信息】")
        resp = self.ownerAction.site()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_网站说明文案(self):
        Pylog.info("【内容管理-网站信息管理-网站说明文案】")
        resp = self.ownerAction.copyright()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_优惠活动(self):
        Pylog.info("【内容管理-优惠活动管理-优惠活动】")
        resp = self.ownerAction.activity()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_轮播图(self):
        Pylog.info("【内容管理-内容发布管理-轮播图】")
        resp = self.ownerAction.carousel()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_公告管理(self):
        Pylog.info("【内容管理-内容发布管理-公告管理】")
        resp = self.ownerAction.notice()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_首页弹屏(self):
        Pylog.info("【内容管理-内容发布管理-首页弹屏】")
        resp = self.ownerAction.popText()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_信息模板(self):
        Pylog.info("【内容管理-站内信管理-信息模板】")
        resp = self.ownerAction.msgTemplate()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

    def test_搜索站内信(self):
        Pylog.info("【内容管理-站内信管理-站内信-搜索站内信】")
        resp = self.content.instationMsg_list()
        dictResp = json.loads(resp)
        totalSize = dictResp['data']['totalSize']
        self.assertGreater(totalSize, 0)

    def test_发送站内信(self):
        Pylog.info("【内容管理-站内信管理-站内信-发送站内信】")
        resp = self.content.instationMsg_save()
        dictResp = json.loads(resp)
        data = dictResp['data']
        self.assertGreater(data, 0)

    def test_公告通知(self):
        Pylog.info("【内容管理-公告通知】")
        resp = self.content.bulletin_list()
        dictResp = json.loads(resp)
        err = dictResp['err']
        self.assertEqual("SUCCESS", err)

if __name__ == "__main__":
    Pylog()
    testsuite = unittest.makeSuite(Ownercase)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(testsuite)

    # Ownercase().test_今日方案()

