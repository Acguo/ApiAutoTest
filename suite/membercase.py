# coding:utf-8
import unittest
from ddt import ddt, data, unpack, file_data

from utils.pylog import Pylog
from action.memberaction import MemberAction
from action.owner.payment import Payment
from action import apiaction
from config import configutil


@ddt
class Membercase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Pylog.info("***************开始执行用例（member）***************")
        cls.config = configutil.Config()
        cls.member = MemberAction()
        cls.membername = "robot005"

    @classmethod
    def tearDownClass(cls):
        Pylog.info("***************结束执行用例（member）***************")

    # @unittest.skip
    def test_01testpley(self):
        Pylog.info("TestCase---------------试玩")
        self.member.do_testplay()

    def test_02creatememner(self):
        Pylog.info("TestCase---------------注册")
        self.member.createMember(username=self.membername)

    @unittest.skip
    def test_03cms(self):
        Pylog.info("TestCase---------------cms_get接口")

    def test_04charge(self):
        Pylog.info("TestCase—充值")
        self.member.charge_company()
        # 业主审核通过
        Payment().chargeCmy_audit(memberName=self.membername)

    def test_05draw(self):
        Pylog.info("TestCase---------------绑卡")
        self.member.saveMemberBank()

    def test_06draw(self):
        Pylog.info("TestCase---------------提款")
        self.member.drawOrder()
        # 业主审核通过
        Payment().draw_audit(memberName=self.membername)

    @data(2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 102, 104, 106, 108, 110)
    def test_07randombet(self, lotteryId):
        Pylog.info("TestCase---------------全部投注")
        datas = apiaction.get_random(lottery=lotteryId)

        test_result = self.member.do_randombet(lotteryid=lotteryId, datas=datas)
        self.assertEqual('', test_result)

        # @file_data(44)
        # def test_ddt(self, data):
        #     print("测试ddt：" + str(data))


if __name__ == "__main__":
    testsuite = unittest.makeSuite(Membercase)
    # filename = "E:\\env\\lottery2\\autotest\\report.html"
    # fp = open(filename, "wb")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(testsuite)
    # fp.close()
