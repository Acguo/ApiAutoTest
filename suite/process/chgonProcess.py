# coding:utf-8
import unittest
import json
import time
from config import globalvars
from utils.pylog import Pylog
from action.memberaction import MemberAction
from action.owner import paramConfig, uaa, payment


class ChgonProcess(unittest.TestCase):
    '''线上入款流程'''

    @classmethod
    def setUpClass(cls):
        Pylog.info("***************开始执行用例（ChgonProcess）***************")
        cls.config = globalvars.config()
        cls.paramConfig = paramConfig.ParamConfig()
        cls.memberaction = MemberAction()
        cls.payment = payment.Payment()
        cls.membername = globalvars.get_value("membername")

    @classmethod
    def tearDownClass(cls):
        Pylog.info("***************结束执行用例（ChgonProcess）***************")

    def test_01_业主上线入款配置_全部停用(self):
        Pylog.info("TestCase---------------test_01_业主上线入款配置_全部停用")
        results = self.paramConfig.thirdpay_statusAll(status=0)
        self.assertIn("SUCCESS", results)

    def test_02_业主上线入款配置_删除(self):
        Pylog.info("TestCase---------------test_02_业主上线入款配置_删除")
        results = self.paramConfig.thirdpay_delete(merchantName="新码支付微信")
        self.assertIn("SUCCESS", results)
        results = self.paramConfig.thirdpay_delete(merchantName="新码支付QQ扫码")
        self.assertIn("SUCCESS", results)

    def test_03_业主上线入款配置_新增(self):
        Pylog.info("TestCase---------------test_03_业主上线入款配置_新增")
        # results = self.paramConfig.thirdpay_create("掌托支付微信", 880800056, "a97d77e568fdda8835599f5035e48645")
        results = self.paramConfig.thirdpay_create("新码支付微信", 180400393344, "8ea8f36a7df6401ba835d66bdd98d7d8")
        self.assertIn("SUCCESS", results)
        # results = self.paramConfig.thirdpay_create("高通支付QQ", 12539, "ed37978aad0bfb1326bb413c44548ce9")
        results = self.paramConfig.thirdpay_create("新码支付QQ扫码", 180400393344, "8ea8f36a7df6401ba835d66bdd98d7d8")

        self.assertIn("SUCCESS", results)

    def test_04_业主上线入款配置_启用(self):
        Pylog.info("TestCase---------------test_04_业主上线入款配置_启用")
        clist1 = self.paramConfig.thirdpay_list(merchantName="新码支付微信")
        clist2 = self.paramConfig.thirdpay_list(merchantName="新码支付QQ扫码")
        clist = json.loads(clist1)["data"]["rows"] + json.loads(clist2)["data"]["rows"]
        for cid in clist:
            results = self.paramConfig.thirdpay_status(cid=cid["id"], status=1)
            self.assertIn("SUCCESS", results)

    def test_05_业主快捷支付配置_全部删除(self):
        Pylog.info("TestCase---------------test_05_业主快捷支付配置_全部删除")
        results = self.paramConfig.receipt_deleteAll()
        self.assertIn("SUCCESS", results)

    def test_06_业主快捷支付配置_新增(self):
        Pylog.info("TestCase---------------test_06_业主快捷支付配置_新增")
        results = self.paramConfig.receipt_create("auto快捷支付", "http://www.58.com")
        self.assertIn("SUCCESS", results)

    def test_07_业主快捷支付配置_全部启用(self):
        Pylog.info("TestCase---------------test_07_业主快捷支付配置_全部启用")
        results = self.paramConfig.receipt_statusAll()
        self.assertIn("SUCCESS", results)

    def test_08_会员快捷支付(self):
        Pylog.info("TestCase---------------test_08_会员快捷支付")
        clist = self.memberaction.charge_client()
        clist = json.loads(clist)["data"]
        for client in clist:
            if client["rsName"] == "auto快捷支付":
                rsUrl = client["rsUrl"]
                self.assertEqual("http://www.58.com", rsUrl)

    def test_09_会员线上支付(self):
        Pylog.info("TestCase---------------test_09_会员线上支付")
        time.sleep(3)
        results = self.memberaction.charge_online("微信支付", 5000)
        self.assertIn("SUCCESS", results)
        results = self.memberaction.charge_online("QQ", 6000)
        self.assertIn("SUCCESS", results)

    def test_10_业主线上入款审核(self):
        Pylog.info("TestCase---------------test_10_业主线上入款审核")
        clist = self.payment.online_chargeList(memberName=self.membername)
        clist = json.loads(clist)["data"]["rows"]
        self.assertEqual(2, len(clist))
        for cid in clist:
            self.payment.online_audit(cid["cid"], 5)
            if clist.index(cid) == 0:
                results = self.payment.online_audit(cid["cid"], 4)
                self.assertIn("SUCCESS", results)
            else:
                results = self.payment.online_audit(cid["cid"], 3)
                self.assertIn("SUCCESS", results)

    def test_11_会员余额验证(self):
        Pylog.info("TestCase---------------test_11_会员余额验证")
        balance = self.memberaction.get_balance()
        balance = json.loads(balance)["data"]["balance"]
        self.assertEqual(int(balance), 330360)

    def test_12_会员入款列表验证(self):
        Pylog.info("TestCase---------------test_12_会员入款列表验证")
        results = self.memberaction.get_tradeList()
        results = json.loads(results)["data"]
        self.assertEqual(11, len(results))

    def test_13_会员稽核验证(self):
        Pylog.info("TestCase---------------test_13_会员稽核验证")
        results = self.memberaction.get_judge()
        results = json.loads(results)["data"]
        auditDeduction = results["auditDeduction"]
        differenceAmount = results["differenceAmount"]
        self.assertEqual(48720, auditDeduction)
        self.assertEqual(2630160, differenceAmount)
