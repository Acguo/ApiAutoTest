# coding:utf-8
import unittest
import json

from config import globalvars
from utils.pylog import Pylog
from action.memberaction import MemberAction
from action.owner import paramConfig, uaa, payment


class ChgoffProcess(unittest.TestCase):
    '''公司入款流程'''

    @classmethod
    def setUpClass(cls):
        Pylog.info("***************开始执行用例（ChgoffProcess）***************")
        cls.config = globalvars.config()
        cls.paramConfig = paramConfig.ParamConfig()
        cls.memberaction = MemberAction()
        cls.uaa = uaa.Uaa()
        cls.payment = payment.Payment()
        cls.membername = globalvars.get_value("membername")

    @classmethod
    def tearDownClass(cls):
        Pylog.info("***************结束执行用例（ChgoffProcess）***************")

    def test_01_业主出入款优惠设定_全部删除(self):
        Pylog.info("TestCase---------------test_01_业主出入款优惠设定_全部删除")
        results = self.paramConfig.accessDiscount_deleteAll()
        self.assertIn("SUCCESS", results)

    def test_02_业主出入款优惠设定_新增(self):
        Pylog.info("TestCase---------------test_02_业主出入款优惠设定_新增")
        results = self.paramConfig.accessDiscount_create("auto出入款优惠vct")
        self.assertIn("SUCCESS", results)
        cid = json.loads(results)["data"]
        globalvars.set_value("accessDiscount_id", cid)

    def test_03_业主层级绑定出入款优惠设定(self):
        Pylog.info("TestCase---------------test_03_业主层级绑定出入款优惠设定")
        # 查询会员层级
        results = self.uaa.member_info(self.membername)
        self.assertIn(self.membername, results)
        levelName = json.loads(results)["data"]["levelName"]
        levelId = json.loads(results)["data"]["levelId"]
        globalvars.set_value("member_level", {"id": levelId, "value": levelName})
        # 更改层级绑定出入款优惠设定
        results = self.uaa.level_bind_acced(levelName, "auto出入款优惠vct", globalvars.get_value("accessDiscount_id"))
        self.assertIn("SUCCESS", results)

    def test_04_业主公司入款设定_全部删除(self):
        Pylog.info("TestCase---------------test_04_业主公司入款设定_全部删除")
        results = self.paramConfig.income_deleteAll()
        self.assertIn("SUCCESS", results)

    def test_05_业主公司入款设定_新增(self):
        Pylog.info("TestCase---------------test_05_业主公司入款设定_新增")
        results = self.paramConfig.income_create(globalvars.get_value("member_level"))
        self.assertIn("SUCCESS", results)

    def test_06_业主公司入款设定_启用(self):
        Pylog.info("TestCase---------------test_06_业主公司入款设定_启用")
        clist = self.paramConfig.income_list()
        clist = json.loads(clist)["data"]["rows"]
        for i in clist:
            results = self.paramConfig.income_status(i["id"], 1)
            self.assertIn("SUCCESS", results)

    def test_07_业主钱包支付配置_全部删除(self):
        Pylog.info("TestCase---------------test_07_业主钱包支付配置_全部删除")
        results = self.paramConfig.walletpay_deleteAll()
        self.assertIn("SUCCESS", results)

    def test_08_业主钱包支付配置_新增(self):
        Pylog.info("TestCase---------------test_08_业主钱包支付配置_新增")
        results = self.paramConfig.walletpay_create(accountType=1)
        self.assertIn("SUCCESS", results)
        results = self.paramConfig.walletpay_create(accountType=2)
        self.assertIn("SUCCESS", results)

    def test_09_业主钱包支付配置_启用(self):
        Pylog.info("TestCase---------------test_09_业主钱包支付配置_启用")
        results = self.paramConfig.walletpay_statusAll(status=1)
        self.assertIn("SUCCESS", results)

    def test_10_H5验证公司入款上下限制(self):
        Pylog.info("TestCase---------------test_10_H5验证公司入款上下限制")
        clientInfo = self.memberaction.charge_client()
        clientInfo = json.loads(clientInfo)["data"]
        for client in clientInfo:
            if client["rsName"] in ["银行转账", "钱包支付"]:
                self.assertEqual(str(700), str(client["minDepositAmount"]))
                self.assertEqual(str(7000000), str(client["maxDepositAmount"]))

    def test_11_H5会员公司入款三笔(self):
        Pylog.info("TestCase---------------test_11_H5会员公司入款三笔")
        results = self.memberaction.charge_company(50000)
        self.assertIn("SUCCESS", results)
        results = self.memberaction.charge_company(100000)
        self.assertIn("SUCCESS", results)
        results = self.memberaction.charge_company(150000)
        self.assertIn("SUCCESS", results)

    def test_12_H5会员钱包秒充2笔(self):
        Pylog.info("TestCase---------------test_12_H5会员钱包秒充2笔")
        results = self.memberaction.charge_walletpay(accountType=1, money=100000)
        self.assertIn("SUCCESS", results)
        results = self.memberaction.charge_walletpay(accountType=2, money=100000)
        self.assertIn("SUCCESS", results)

    def test_13_业主公司入款审核(self):
        Pylog.info("TestCase---------------test_13_业主公司入款审核")
        clist = self.payment.offline_chargeList(memberName=self.membername)
        clist = json.loads(clist)["data"]["rows"]
        self.assertEqual(5, len(clist))
        for item in clist:
            cid = item["cid"]
            self.payment.offline_audit(id=cid, state=5)
            if clist.index(item) in [0, 1, 3]:
                results = self.payment.offline_audit(id=cid, state=4)
                self.assertIn("SUCCESS", results)
            elif clist.index(item) == 2:
                results = self.payment.offline_audit(id=cid, state=3)
                self.assertIn("SUCCESS", results)
