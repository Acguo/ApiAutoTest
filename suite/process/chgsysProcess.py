# coding:utf-8
import unittest
import json
import time

from config import globalvars
from utils.pylog import Pylog
from action.memberaction import MemberAction
from action.owner import payment


class ChgsysProcess(unittest.TestCase):
    '''人工出入款流程'''

    @classmethod
    def setUpClass(cls):
        Pylog.info("***************开始执行用例（ChgsysProcess）***************")
        cls.config = globalvars.config()
        cls.memberaction = MemberAction()
        cls.payment = payment.Payment()
        cls.membername = globalvars.get_value("membername")

    @classmethod
    def tearDownClass(cls):
        Pylog.info("***************结束执行用例（ChgsysProcess）***************")

    def test_01_人工入款_人工存款(self):
        Pylog.info("TestCase---------------test_01_人工入款_人工存款")
        results = self.payment.system_charge(self.membername, "人工存款")
        self.assertIn("SUCCESS", results)

    def test_02_人工入款_活动优惠(self):
        Pylog.info("TestCase---------------test_02_人工入款_活动优惠")
        results = self.payment.system_charge(self.membername, "活动优惠")
        self.assertIn("SUCCESS", results)

    def test_03_人工入款_其他入款(self):
        Pylog.info("TestCase---------------test_03_人工入款_其他入款")
        results = self.payment.system_charge(self.membername, "其他入款")
        self.assertIn("SUCCESS", results)

    def test_04_业主稽核验证(self):
        Pylog.info("TestCase---------------test_04_业主稽核验证")
        time.sleep(3)
        auditInfo = self.payment.member_audit(self.membername)
        auditInfo = json.loads(auditInfo)["data"]["immediateAudit"]
        self.assertEqual(7, len(auditInfo["detailsList"]))
        self.assertEqual(326000, auditInfo["totalNormalAuditAmount"])
        self.assertEqual(326000, auditInfo["totalTradeAmount"])
        self.assertEqual(35360, auditInfo["totalDiscountAmount"])
        self.assertEqual(2672160, auditInfo["totalDiscountAuditAmount"])
        self.assertEqual(35360, auditInfo["discountDeduction"])
        self.assertEqual(26360, auditInfo["administrativeFeeDeduction"])

    def test_05_人工提出_手动申请出款(self):
        Pylog.info("TestCase---------------test_05_人工提出_手动申请出款")
        results = self.payment.system_draw(self.membername, "手动申请出款")
        self.assertIn("SUCCESS", results)

    def test_06_人工提出_其他出款(self):
        Pylog.info("TestCase---------------test_06_人工提出_其他出款")
        results = self.payment.system_draw(self.membername, "其他出款")
        self.assertIn("SUCCESS", results)

    def test_07_人工存提记录(self):
        Pylog.info("TestCase---------------test_07_人工存提记录")
        resultschg = self.payment.chargeanddraw_record(self.membername, "人工存入")
        resultsdraw = self.payment.chargeanddraw_record(self.membername, "人工提出")
        totalAmountchg = json.loads(resultschg)["summary"]["totalAmount"]
        totalAmountdraw = json.loads(resultsdraw)["summary"]["totalAmount"]
        self.assertEqual(31000, totalAmountchg)
        self.assertEqual(20000, totalAmountdraw)
        self.assertIn("auto备注人工存款1", resultschg)
        self.assertIn("auto备注人工存款2", resultschg)
        self.assertIn("auto备注活动优惠", resultschg)
        self.assertIn("auto备注其他入款", resultschg)

        self.assertIn("auto备注手动申请出款", resultsdraw)
        self.assertIn("auto备注其他出款", resultsdraw)
        self.assertIn("常态稽核、优惠稽", resultsdraw)

    def test_08_业主金流查询(self):
        Pylog.info("TestCase---------------test_08_业主金流查询")
        results = self.payment.cashFlow_list(self.membername)
        self.assertIn("已补单", results)
        self.assertIn("auto备注活动优惠", results)
        self.assertIn("auto备注手动申请出款", results)
        self.assertIn("auto备注人工存款2", results)
        self.assertIn("auto备注人工存款1", results)
        results = json.loads(results)["data"]
        self.assertEqual(14, len(results["rows"]))

    def test_09_会员余额验证(self):
        Pylog.info("TestCase---------------test_11_会员余额验证")
        balance = self.memberaction.get_balance()
        balance = json.loads(balance)["data"]["balance"]
        self.assertEqual(int(balance), 341360)