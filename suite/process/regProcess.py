# coding:utf-8
import unittest
import time
import json

from config import globalvars
from utils.pylog import Pylog
from action.memberaction import MemberAction
from action.owner import paramConfig, uaa


class RegProcess(unittest.TestCase):
    '''注册会员流程'''
    @classmethod
    def setUpClass(cls):
        Pylog.info("***************开始执行用例（RegProcess）***************")
        cls.config = globalvars.config()
        cls.paramConfig = paramConfig.ParamConfig()
        cls.uaa = uaa.Uaa()
        cls.memberaction = MemberAction()

        cls.membername = globalvars.get_value("membername")

    @classmethod
    def tearDownClass(cls):
        Pylog.info("***************结束执行用例（RegProcess）***************")

    def test_01_业主注册配置(self):
        Pylog.info("TestCase---------------test_01_业主注册配置")
        datas = self.paramConfig.registerConfig_list()
        self.assertIn("version", str(datas))

        results = self.paramConfig.registerConfig_save(datas)
        self.assertIn("SUCCESS", results)

    def test_02_业主同IP注册限制配置(self):
        Pylog.info("TestCase---------------test_02_业主同IP注册限制配置")
        results = self.paramConfig.reg_sameIp(1, 3, 1)
        self.assertIn("SUCCESS", results)

    def test_03_业主注册优惠配置_全部删除(self):
        Pylog.info("TestCase---------------test_03_业主注册优惠配置_全部删除")
        results = self.paramConfig.registDiscount_deleteAll()
        self.assertIn("SUCCESS", results)

    def test_04_业主注册优惠配置_新增(self):
        Pylog.info("TestCase---------------test_03_业主注册优惠配置_新增")
        model = self.config.model("owner", "agentChgInfo.json")
        origin = self.config.owner["env"]["origin_mb"]
        # 查询域名列表、所属代理
        domainInfo = self.paramConfig.domain_list(domain=origin)
        self.assertIn("agentAccount", domainInfo)
        agentAccount = json.loads(domainInfo)["data"]["rows"][0]["agentAccount"]
        agentInfo = self.uaa.agent_info(agentname=agentAccount)
        self.assertIn(agentAccount, agentInfo)
        # 新增注册配置
        cid = self.paramConfig.registDiscount_create(name="auto注册优惠vct", money=10, audit=2)
        self.assertIsInstance(cid, int)

        agentInfo = json.loads(agentInfo)["data"]
        model["administrativeId"] = agentInfo["administrativeId"]
        model["cid"] = agentInfo["agentId"]
        model["feePlanId"] = agentInfo["feePlanId"]
        model["memberLevelId"] = agentInfo["memberLevelId"]
        model["preferentialCost"] = agentInfo["preferentialCost"]
        model["rebateCost"] = agentInfo["rebateCost"]
        model["retirementId"] = agentInfo["retirementId"]
        model["registerDiscountId"] = cid
        # 代理绑定注册配置
        results = self.uaa.agent_chgInfo(model)
        self.assertIn("SUCCESS", results)

    def test_05_H5验证注册配置(self):
        Pylog.info("TestCase---------------test_04_H5验证注册配置")
        regconfig = globalvars.get_value("regconfig")
        results = self.memberaction.getconfig_reg()
        results = json.loads(results)["data"]
        self.assertListEqual(regconfig, results)

    def test_06_H5验证同IP注册限制(self):
        Pylog.info("TestCase---------------test_05_H5验证同IP注册限制")
        for i in range(0, 4):
            results = self.memberaction.createMember("ip" + str(time.time()).replace(".", ""))
        self.assertIn("本IP注册人数已达上限", results)

        results = self.paramConfig.reg_sameIp(1, 3, 0)
        self.assertIn("SUCCESS", results)

    def test_07_H5正向注册(self):
        Pylog.info("TestCase---------------test_06_H5正向注册")
        time.sleep(2)
        results = self.memberaction.createMember(username=self.membername)
        self.assertIn("access_token", results)

    def test_08_H5登陆(self):
        Pylog.info("TestCase---------------test_07_H5登陆")
        results = self.memberaction.login(self.membername)
        self.assertIn("access_token", results)

    def test_09_H5验证注册优惠(self):
        Pylog.info("TestCase---------------test_07_H5验证注册优惠")
        results = self.uaa.memberList(self.membername)
        balance = json.loads(results)["rows"][0]["balance"]
        self.assertEqual(float(balance) / 100, float(10))
