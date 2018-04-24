# coding:utf-8
import unittest
import json
import time
from config import globalvars
from utils.pylog import Pylog
from action.memberaction import MemberAction
from action.owner import payment, statistics


class DrawProcess(unittest.TestCase):
    '''会员提款流程'''

    @classmethod
    def setUpClass(cls):
        Pylog.info("***************开始执行用例（DrawProcess）***************")
        cls.memberaction = MemberAction()
        cls.payment = payment.Payment()
        cls.statistics = statistics.Statistics()
        cls.membername = globalvars.get_value("membername")

    @classmethod
    def tearDownClass(cls):
        Pylog.info("***************结束执行用例（DrawProcess）***************")

    def test_01_会员绑卡(self):
        Pylog.info("TestCase---------------test_01_会员绑卡")
        results = self.memberaction.saveMemberBank()
        self.assertIn("SUCCESS", results)

    def test_02_会员更改提款密码(self):
        Pylog.info("TestCase---------------test_02_会员更改提款密码")
        results = self.memberaction.changeDrawPwd("1234", "1111")
        self.assertIn("SUCCESS", results)

    def test_03_会员提款_密码校验(self):
        Pylog.info("TestCase---------------test_03_会员提款_密码校验")
        results = self.memberaction.drawOrder(money=10000, pwd="1234")
        self.assertIn("取款密码错误", results)

    def test_04_会员提款_提款金额范围校验(self):
        Pylog.info("TestCase---------------test_04_会员提款_提款金额范围校验")
        results = self.memberaction.drawOrder(money=300, pwd="1111")
        self.assertIn("FAILED", results)
        results = self.memberaction.drawOrder(money=500000, pwd="1111")
        self.assertIn("FAILED", results)
        results = self.memberaction.drawOrder(money=2000000, pwd="1111")
        self.assertIn("FAILED", results)

    def test_05_会员提款(self):
        Pylog.info("TestCase---------------test_05_会员提款")
        results = self.memberaction.drawOrder(money=10000, pwd="1111")
        self.assertIn("SUCCESS", results)
        results = self.memberaction.drawOrder(money=20000, pwd="1111")
        self.assertIn("SUCCESS", results)
        results = self.memberaction.drawOrder(money=30000, pwd="1111")
        self.assertIn("SUCCESS", results)

    def test_06_业主提款审核(self):
        Pylog.info("TestCase---------------test_06_业主提款审核")
        bind_data = globalvars.get_value("bind_data")
        results = self.payment.draw_list(memberName=self.membername)
        results = json.loads(results)["data"]["rows"]
        self.assertEqual(3, len(results))
        for row in results:
            self.assertEqual(bind_data["bankCard"], row["cardNo"])
            self.assertEqual(bind_data["realName"], row["realName"])
            self.payment.draw_audit(row["cid"], 5)
            if results.index(row) == 0:
                self.payment.draw_audit(row["cid"], 3)
            elif results.index(row) == 2:
                self.payment.draw_audit(row["cid"], 4)

    def test_07_会员余额验证(self):
        Pylog.info("TestCase---------------test_07_会员余额验证")
        balance = self.memberaction.get_balance()
        balance = json.loads(balance)["data"]["balance"]
        self.assertEqual(int(balance), 311360)

    def test_08_会员出款列表验证(self):
        Pylog.info("TestCase---------------test_08_会员出款列表验证")
        results = self.memberaction.get_tradeList(searchType=3)
        datas = json.loads(results)["data"]
        self.assertEqual(5, len(datas))
        self.assertIn("失败", results)
        self.assertIn("处理中", results)

    def test_09_业主出入款统计(self):
        Pylog.info("TestCase---------------test_09_业主出入款统计")
        starttime = time.strftime("%Y-%m-%d", time.gmtime()) + " 00:00:00"
        endtime = time.strftime("%Y-%m-%d", time.gmtime()) + " 23:59:59"
        results = self.statistics.statistics_inout(self.membername, starttime, endtime)
        results = json.loads(results)["data"]["rows"][0]
        self.assertEqual(6, results["inMoneyTimes"])
        self.assertEqual(326000, results["inMoneyAmount"])
        self.assertEqual(3, results["outMoneyTimes"])
        self.assertEqual(30000, results["outMoneyAmount"])