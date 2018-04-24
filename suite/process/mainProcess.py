# coding:utf-8
import unittest
import json
import random
import time
from ddt import ddt, data, unpack, file_data

from utils.pylog import Pylog
from auth.authors import Authors
from action.memberaction import MemberAction
from action.owner.payment import Payment
from action.owner.paramConfig import ParamConfig
from action.owner.content import Content
from action.owner.uaa import Uaa
from action.memberBet import MemberBet
from config import globalvars


# @ddt
class MainProcess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Pylog.info("***************开始执行用例（member）***************")
        cls.config = globalvars.config()
        cls.loId_list = cls.config.model("member", "lotteryId.json")
        Authors("owner")
        cls.payment = Payment()
        cls.paramconfig = ParamConfig()
        cls.uaa = Uaa()
        cls.memberbet = MemberBet()
        cls.content = Content()
        cls.member = MemberAction()
        cls.membername = "cs_05"
        globalvars.set_value("membername", cls.membername)

    @classmethod
    def tearDownClass(cls):
        Pylog.info("***************结束执行用例（member）***************")

    # @unittest.skip
    def test_01试玩(self):
        Pylog.info("TestCase---------------test_01试玩")
        results = self.member.do_testplay()
        self.assertIn("SUCCESS", results)

    def test_02_01注册设定配置(self):
        Pylog.info("TestCase---------------test_02_01注册设定配置")
        datas = self.paramconfig.registerConfig_list()

        for i in datas:
            i["ifCheck"] = 0
        self.paramconfig.registerConfig_save(datas)

    def test_02_02注册正向场景(self):
        Pylog.info("TestCase---------------test_02_02注册正向场景")
        results = self.member.createMember(username=self.membername)
        self.assertIn("SUCCESS", results)

    def test_03登陆(self):
        Pylog.info("TestCase---------------test_03登陆")
        results = self.member.login(userName=self.membername)
        self.assertIn("SUCCESS", results)

    def test_04_00出入款优惠设定(self):
        Pylog.info("TestCase---------------test_04_00出入款优惠设定")
        results = self.uaa.member_info(self.membername)
        self.assertIn("SUCCESS", results)
        cid = json.loads(results)["data"]["accessDiscount"]["cid"]
        title = json.loads(results)["data"]["accessDiscount"]["title"]
        results = self.paramconfig.accessDiscount_save(cid)
        self.assertIn("SUCCESS", results)

    def test_04_01启用公司入款账号(self):
        Pylog.info("TestCase---------------test_04_01启用公司入款账号")
        results = self.paramconfig.income_status()
        self.assertIn("SUCCESS", results)

    def test_04_02会员入款公司入款(self):
        Pylog.info("TestCase---------------test_04_02会员入款公司入款")
        results = self.member.charge_company(100000)
        self.assertIn("SUCCESS", results)
        results = self.member.charge_company(100000)
        self.assertIn("SUCCESS", results)

    def test_04_03公司入款优惠验证(self):
        Pylog.info("TestCase---------------test_04_03公司入款优惠验证")



    def test_04_04公司入款后台审核通过(self):
        Pylog.info("TestCase---------------test_04_04公司入款后台审核通过")
        cid = json.loads(self.payment.offline_chargeList(memberName=self.membername))["data"]["rows"][0]["cid"]
        self.payment.offline_audit(id=cid, state=5)
        results = self.payment.offline_audit(id=cid, state=4)
        self.assertIn("SUCCESS", results)

    def test_04_05公司入款后台审核不通过(self):
        Pylog.info("TestCase---------------test_04_04公司入款后台审核不通过")
        cid = json.loads(self.payment.offline_chargeList(memberName=self.membername))["data"]["rows"][0]["cid"]
        self.payment.offline_audit(id=cid, state=5)
        results = self.payment.offline_audit(id=cid, state=3)
        self.assertIn("SUCCESS", results)

    def test_05绑卡(self):
        Pylog.info("TestCase---------------test_05绑卡")
        results = self.member.saveMemberBank()
        self.assertIn("SUCCESS", results)

    def test_06_01会员提款(self):
        Pylog.info("TestCase---------------test_06_01会员提款")
        results = self.member.drawOrder()
        self.assertIn("SUCCESS", results)

    def test_06_02会员提款审核通过(self):
        Pylog.info("TestCase---------------test_06_02会员提款审核通过")
        drawDatas = json.loads(self.payment.draw_list(memberName=self.membername))["data"]["rows"][0]
        cid = drawDatas["cid"]
        bind_data = globalvars.get_value("bind_data")
        self.assertEqual(bind_data["bankCard"], drawDatas["cardNo"])
        self.assertEqual(bind_data["realName"], drawDatas["realName"])
        Pylog.info("会员提款审核: 验证提款人信息ok")
        self.payment.draw_audit(id=cid, state=5)
        results = self.payment.draw_audit(id=cid, state=4)
        self.assertIn("SUCCESS", results)

    def test_07_01cms站内信配置(self):
        Pylog.info("TestCase---------------test_07_01cms站内信配置")
        results = self.content.instationMsg_save("测试数据test data！！")
        self.assertIn("SUCCESS", results)

    def test_07_02cms站内信验证(self):
        Pylog.info("TestCase---------------test_07_02cms站内信验证")
        time.sleep(2)
        results = self.member.get_msg()
        self.assertIn("测试数据test data！！", results)

    def test_08_01cms轮播图配置(self):
        Pylog.info("TestCase---------------test_08_01cms轮播图配置")
        results = self.content.carousel_save("http://www.huaban.com")
        self.assertIn("SUCCESS", results)

    def test_08_02cms轮播图验证(self):
        Pylog.info("TestCase---------------test_08_02cms轮播图验证")
        time.sleep(2)
        results = self.member.get_carousel()
        self.assertIn("http://www.huaban.com", results)

    def test_09_01cms首页弹屏配置(self):
        Pylog.info("TestCase---------------test_09_01cms首页弹屏配置")
        results = self.content.popText_create("自动化测试回归数据:首页弹屏!")
        self.assertIn("SUCCESS", results)

    def test_09_02cms首页弹屏验证(self):
        Pylog.info("TestCase---------------test_09_02cms首页弹屏验证")
        time.sleep(2)
        results = self.member.get_popText()
        self.assertIn("自动化测试回归数据:首页弹屏!", results)

    def test_10_01cms公告配置(self):
        Pylog.info("TestCase---------------test_10_01cms公告配置")
        results = self.content.notice_create("自动化测试回归数据:首页公告!")
        self.assertIn("SUCCESS", results)

    def test_10_02cms公告验证(self):
        Pylog.info("TestCase---------------test_10_02cms公告验证")
        time.sleep(2)
        results = self.member.get_notice()
        self.assertIn("自动化测试回归数据:首页公告!", results)

    def test_11_01cms优惠活动配置(self):
        Pylog.info("TestCase---------------test_11_01cms优惠活动配置")
        results = self.content.activity_save("自动化测试回归数据:优惠活动！")
        self.assertIn("SUCCESS", results)

    def test_11_02cms优惠活动验证(self):
        Pylog.info("TestCase---------------test_11_02cms优惠活动验证")
        time.sleep(2)
        cid = globalvars.get_value("activity_cid")
        results = self.member.get_activity(cid)
        self.assertIn("自动化测试回归数据:优惠活动！", results)

    def test_12_01投注时时彩(self):
        lists = self.loId_list["ssc"]
        lotteryId = random.choice(lists)
        Pylog.info("TestCase---------------test_12_01投注时时彩(lotteryID:{})".format(str(lotteryId)))
        results = self.memberbet.pre_bet(lotteryId)
        self.assertEqual("SUCCESS", results)
        lists.remove(lotteryId)
        lotteryId_2 = random.choice(lists)
        Pylog.info("TestCase---------------test_12_01投注时时彩(lotteryID:{})".format(str(lotteryId_2)))
        results = self.memberbet.pre_bet(lotteryId_2)
        self.assertEqual("SUCCESS", results)

    def test_12_02投注快三(self):
        lists = self.loId_list["k3"]
        lotteryId = random.choice(lists)
        Pylog.info("TestCase---------------test_12_02投注快三(lotteryID:{})".format(str(lotteryId)))
        results = self.memberbet.pre_bet(lotteryId)
        self.assertEqual("SUCCESS", results)
        lists.remove(lotteryId)
        lotteryId_2 = random.choice(lists)
        Pylog.info("TestCase---------------test_12_02投注快三(lotteryID:{})".format(str(lotteryId_2)))
        results = self.memberbet.pre_bet(lotteryId_2)
        self.assertEqual("SUCCESS", results)

    def test_12_03投注11选5(self):
        lists = self.loId_list["11x5"]
        lotteryId = random.choice(lists)
        Pylog.info("TestCase---------------test_12_03投注11选5(lotteryID:{})".format(str(lotteryId)))
        results = self.memberbet.pre_bet(lotteryId)
        self.assertEqual("SUCCESS", results)
        lists.remove(lotteryId)
        lotteryId_2 = random.choice(lists)
        Pylog.info("TestCase---------------test_12_03投注11选5(lotteryID:{})".format(str(lotteryId_2)))
        results = self.memberbet.pre_bet(lotteryId_2)
        self.assertEqual("SUCCESS", results)

    def test_12_04投注赛车系列(self):
        lists = self.loId_list["pk10"]
        lotteryId = random.choice(lists)
        Pylog.info("TestCase---------------test_12_04投注赛车系列(lotteryID:{})".format(str(lotteryId)))
        results = self.memberbet.pre_bet(lotteryId)
        self.assertEqual("SUCCESS", results)
        lists.remove(lotteryId)
        lotteryId_2 = random.choice(lists)
        Pylog.info("TestCase---------------test_12_04投注赛车系列(lotteryID:{})".format(str(lotteryId_2)))
        results = self.memberbet.pre_bet(lotteryId_2)
        self.assertEqual("SUCCESS", results)

    def test_12_05投注六合彩系列(self):
        Pylog.info("TestCase---------------test_12_05投注六合彩系列(lotteryID:{})".format(str(10)))
        results = self.memberbet.pre_bet(10)
        self.assertEqual("SUCCESS", results)
        Pylog.info("TestCase---------------test_12_05投注六合彩系列(lotteryID:{})".format(str(110)))
        results = self.memberbet.pre_bet(110)
        self.assertEqual("SUCCESS", results)

        # Pylog.info("test_07_01cms取配置: 优惠活动")
        # Pylog.info("test_07_01cms取配置: 新手教程")
        # Pylog.info("test_07_01cms取配置: 代理加盟")
        # Pylog.info("test_07_01cms取配置: 关于我们")
