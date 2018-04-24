# coding:utf-8
import unittest
import json

from config import globalvars
from utils.pylog import Pylog
from action.control import lotteryConfig


class CtconfigProcess(unittest.TestCase):
    '''主控配置系列流程'''

    @classmethod
    def setUpClass(cls):
        Pylog.info("***************开始执行用例（BetProcess）***************")
        cls.config = globalvars.config()
        cls.membername = globalvars.get_value("membername")
        cls.LotteryConfig = lotteryConfig.LotteryConfig()

    @classmethod
    def tearDownClass(cls):
        Pylog.info("***************结束执行用例（BetProcess）***************")

    def test_01_主控投注限制_全部停用(self):
        Pylog.info("TestCase---------------test_01_主控投注限制_全部停用")
        results = self.LotteryConfig.quotaLimit_statusAll(0)
        self.assertEqual("SUCCESS", results)

    def test_02_主控异常方案设定_全部停用(self):
        Pylog.info("TestCase---------------test_01_主控投注限制_全部停用")
        results = self.LotteryConfig.orderExp_statusAll(1)
        self.assertEqual("SUCCESS", results)
