# coding:utf-8
import unittest
import json

from utils import utils
from config import globalvars
from utils.pylog import Pylog
from action import memberaction, memberBet
from action.owner import order
from action.control import lotteryConfig


class BetProcess(unittest.TestCase):
    '''投注系列流程'''

    @classmethod
    def setUpClass(cls):
        Pylog.info("***************开始执行用例（BetProcess）***************")
        cls.config = globalvars.config()
        cls.membername = globalvars.get_value("membername")
        cls.memberaction = memberaction.MemberAction()
        cls.memberaction.login(cls.membername)
        cls.order = order.Order()
        cls.bet = memberBet.MemberBet()
        cls.control = lotteryConfig.LotteryConfig()

    @classmethod
    def tearDownClass(cls):
        Pylog.info("***************结束执行用例（BetProcess）***************")

    def test_01_会员投注ssc_重庆时时彩_赔率验证(self):
        Pylog.info("TestCase---------------test_01_会员投注ssc_重庆时时彩_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 2:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(2, odds)
        self.assertIn("SUCCESS", results)

    def test_02_会员投注ssc_重庆时时彩_投注(self):
        Pylog.info("TestCase---------------test_02_会员投注ssc_重庆时时彩_投注")
        results = self.bet.pre_bet(lotteryId=2)
        self.assertEqual("SUCCESS", results)

    def test_03_会员投注ssc_天津时时彩彩_赔率验证(self):
        Pylog.info("TestCase---------------test_03_会员投注ssc_天津时时彩彩_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 12:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(12, odds)
        self.assertIn("SUCCESS", results)

    def test_04_会员投注ssc_天津时时彩彩_投注(self):
        Pylog.info("TestCase---------------test_04_会员投注ssc_天津时时彩彩_投注")
        results = self.bet.pre_bet(lotteryId=12)
        self.assertEqual("SUCCESS", results)

    def test_05_会员投注ssc_新疆时时彩彩_赔率验证(self):
        Pylog.info("TestCase---------------test_05_会员投注ssc_新疆时时彩彩_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 14:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(14, odds)
        self.assertIn("SUCCESS", results)

    def test_06_会员投注ssc_新疆时时彩彩_投注(self):
        Pylog.info("TestCase---------------test_06_会员投注ssc_新疆时时彩彩_投注")
        results = self.bet.pre_bet(lotteryId=14)
        self.assertEqual("SUCCESS", results)

    def test_07_会员投注ssc_北京时时彩_赔率验证(self):
        Pylog.info("TestCase---------------test_07_会员投注ssc_北京时时彩_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 26:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(26, odds)
        self.assertIn("SUCCESS", results)

    def test_08_会员投注ssc_北京时时彩_投注(self):
        Pylog.info("TestCase---------------test_08_会员投注ssc_北京时时彩_投注")
        results = self.bet.pre_bet(lotteryId=26)
        self.assertEqual("SUCCESS", results)

    def test_09_会员投注ssc_台湾5分彩_赔率验证(self):
        Pylog.info("TestCase---------------test_09_会员投注ssc_台湾5分彩_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 28:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(28, odds)
        self.assertIn("SUCCESS", results)

    def test_10_会员投注ssc_台湾5分彩_投注(self):
        Pylog.info("TestCase---------------test_10_会员投注ssc_台湾5分彩_投注")
        results = self.bet.pre_bet(lotteryId=28)
        self.assertEqual("SUCCESS", results)

    def test_11_会员投注ssc_QQ分分彩_赔率验证(self):
        Pylog.info("TestCase---------------test_11_会员投注ssc_QQ分分彩_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 32:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(32, odds)
        self.assertIn("SUCCESS", results)

    def test_12_会员投注ssc_QQ分分彩_投注(self):
        Pylog.info("TestCase---------------test_12_会员投注ssc_QQ分分彩_投注")
        results = self.bet.pre_bet(lotteryId=32)
        self.assertEqual("SUCCESS", results)

    def test_13_会员投注ssc_秒速时时彩_赔率验证(self):
        Pylog.info("TestCase---------------test_13_会员投注ssc_秒速时时彩_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 102:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(102, odds)
        self.assertIn("SUCCESS", results)

    def test_14_会员投注ssc_秒速时时彩_投注(self):
        Pylog.info("TestCase---------------test_14_会员投注ssc_秒速时时彩_投注")
        results = self.bet.pre_bet(lotteryId=102)
        self.assertEqual("SUCCESS", results)

    def test_15_会员投注ssc_韩国15分彩_赔率验证(self):
        Pylog.info("TestCase---------------test_15_会员投注ssc_韩国15分彩_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 112:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(112, odds)
        self.assertIn("SUCCESS", results)

    def test_16_会员投注ssc_韩国15分彩_投注(self):
        Pylog.info("TestCase---------------test_16_会员投注ssc_韩国15分彩_投注")
        results = self.bet.pre_bet(lotteryId=112)
        self.assertEqual("SUCCESS", results)

    def test_17_会员投注ssc_东京15分彩_赔率验证(self):
        Pylog.info("TestCase---------------test_17_会员投注ssc_东京15分彩_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 114:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(114, odds)
        self.assertIn("SUCCESS", results)

    def test_18_会员投注ssc_东京15分彩_投注(self):
        Pylog.info("TestCase---------------test_18_会员投注ssc_东京15分彩_投注")
        results = self.bet.pre_bet(lotteryId=114)
        self.assertEqual("SUCCESS", results)

    def test_19_会员投注11x5_江西11选5_赔率验证(self):
        Pylog.info("TestCase---------------test_19_会员投注11x5_江西11选5_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 4:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(4, odds)
        self.assertIn("SUCCESS", results)

    def test_20_会员投注11x5_江西11选5_投注(self):
        Pylog.info("TestCase---------------test_20_会员投注11x5_江西11选5_投注")
        results = self.bet.pre_bet(lotteryId=4)
        self.assertEqual("SUCCESS", results)

    def test_21_会员投注11x5_广东11选5_赔率验证(self):
        Pylog.info("TestCase---------------test_21_会员投注11x5_广东11选5_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 16:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(16, odds)
        self.assertIn("SUCCESS", results)

    def test_22_会员投注11x5_广东11选5_投注(self):
        Pylog.info("TestCase---------------test_22_会员投注11x5_广东11选5_投注")
        results = self.bet.pre_bet(lotteryId=16)
        self.assertEqual("SUCCESS", results)

    def test_23_会员投注11x5_山东11选5_赔率验证(self):
        Pylog.info("TestCase---------------test_23_会员投注11x5_山东11选5_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 18:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(18, odds)
        self.assertIn("SUCCESS", results)

    def test_24_会员投注11x5_山东11选5_投注(self):
        Pylog.info("TestCase---------------test_24_会员投注11x5_山东11选5_投注")
        results = self.bet.pre_bet(lotteryId=18)
        self.assertEqual("SUCCESS", results)

    def test_25_会员投注11x5_秒速11选5_赔率验证(self):
        Pylog.info("TestCase---------------test_25_会员投注11x5_秒速11选5_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 104:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(104, odds)
        self.assertIn("SUCCESS", results)

    def test_26_会员投注11x5_秒速11选5_投注(self):
        Pylog.info("TestCase---------------test_26_会员投注11x5_秒速11选5_投注")
        results = self.bet.pre_bet(lotteryId=104)
        self.assertEqual("SUCCESS", results)

    def test_27_会员投注k3_江苏快3_赔率验证(self):
        Pylog.info("TestCase---------------test_27_会员投注k3_江苏快3_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 6:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(6, odds)
        self.assertIn("SUCCESS", results)

    def test_28_会员投注k3_江苏快3_投注(self):
        Pylog.info("TestCase---------------test_28_会员投注k3_江苏快3_投注")
        results = self.bet.pre_bet(lotteryId=6)
        self.assertEqual("SUCCESS", results)

    def test_29_会员投注k3_安徽快3_赔率验证(self):
        Pylog.info("TestCase---------------test_29_会员投注k3_安徽快3_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 20:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(20, odds)
        self.assertIn("SUCCESS", results)

    def test_30_会员投注k3_安徽快3_投注(self):
        Pylog.info("TestCase---------------test_30_会员投注k3_安徽快3_投注")
        results = self.bet.pre_bet(lotteryId=20)
        self.assertEqual("SUCCESS", results)

    def test_31_会员投注k3_湖北快3_赔率验证(self):
        Pylog.info("TestCase---------------test_31_会员投注k3_湖北快3_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 22:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(22, odds)
        self.assertIn("SUCCESS", results)

    def test_32_会员投注k3_湖北快3_投注(self):
        Pylog.info("TestCase---------------test_32_会员投注k3_湖北快3_投注")
        results = self.bet.pre_bet(lotteryId=22)
        self.assertEqual("SUCCESS", results)

    def test_33_会员投注k3_秒速快3_赔率验证(self):
        Pylog.info("TestCase---------------test_33_会员投注k3_秒速快3_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 106:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(106, odds)
        self.assertIn("SUCCESS", results)

    def test_34_会员投注k3_秒速快3_投注(self):
        Pylog.info("TestCase---------------test_34_会员投注k3_秒速快3_投注")
        results = self.bet.pre_bet(lotteryId=106)
        self.assertEqual("SUCCESS", results)

    def test_35_会员投注pk10_北京PK10_赔率验证(self):
        Pylog.info("TestCase---------------test_35_会员投注pk10_北京PK10_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 8:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(8, odds)
        self.assertIn("SUCCESS", results)

    def test_36_会员投注pk10_北京PK10_投注(self):
        Pylog.info("TestCase---------------test_36_会员投注pk10_北京PK10_投注")
        results = self.bet.pre_bet(lotteryId=8)
        self.assertEqual("SUCCESS", results)

    def test_37_会员投注pk10_幸运飞艇_赔率验证(self):
        Pylog.info("TestCase---------------test_37_会员投注pk10_幸运飞艇_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 24:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(24, odds)
        self.assertIn("SUCCESS", results)

    def test_38_会员投注pk10_幸运飞艇_投注(self):
        Pylog.info("TestCase---------------test_38_会员投注pk10_幸运飞艇_投注")
        results = self.bet.pre_bet(lotteryId=24)
        self.assertEqual("SUCCESS", results)

    def test_39_会员投注pk10_秒速赛车_赔率验证(self):
        Pylog.info("TestCase---------------test_39_会员投注pk10_秒速赛车_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 108:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(108, odds)
        self.assertIn("SUCCESS", results)

    def test_40_会员投注pk10_秒速赛车_投注(self):
        Pylog.info("TestCase---------------test_40_会员投注pk10_秒速赛车_投注")
        results = self.bet.pre_bet(lotteryId=108)
        self.assertEqual("SUCCESS", results)

    def test_41_会员投注lhc_香港六合彩_赔率验证(self):
        Pylog.info("TestCase---------------test_41_会员投注lhc_香港六合彩_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 10:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(10, odds)
        self.assertIn("SUCCESS", results)

    def test_42_会员投注lhc_香港六合彩_投注(self):
        Pylog.info("TestCase---------------test_42_会员投注lhc_香港六合彩_投注")
        results = self.bet.pre_bet(lotteryId=10)
        self.assertEqual("SUCCESS", results)

    def test_43_会员投注lhc_五分香港六合彩_赔率验证(self):
        Pylog.info("TestCase---------------test_43_会员投注lhc_五分香港六合彩_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 110:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(110, odds)
        self.assertIn("SUCCESS", results)

    def test_44_会员投注lhc_五分香港六合彩_投注(self):
        Pylog.info("TestCase---------------test_44_会员投注lhc_五分香港六合彩_投注")
        results = self.bet.pre_bet(lotteryId=110)
        self.assertEqual("SUCCESS", results)

    def test_45_会员投注幸运28_赔率验证(self):
        Pylog.info("TestCase---------------test_45_会员投注幸运28_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 30:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(30, odds)
        self.assertIn("SUCCESS", results)

    def test_46_会员投注幸运28_投注(self):
        Pylog.info("TestCase---------------test_46_会员投注幸运28_投注")
        results = self.bet.pre_bet(lotteryId=30)
        self.assertEqual("SUCCESS", results)

    def test_47_会员投注mmc_重庆秒秒彩_赔率验证(self):
        Pylog.info("TestCase---------------test_47_会员投注mmc_重庆秒秒彩_赔率验证")
        oddsId = self.control.get_plat2odds()
        self.assertIn("SUCCESS", oddsId)
        oddsId = json.loads(oddsId)["data"]["oddsGroup"]
        for odd in oddsId:
            if odd["lotteryId"] == 116:
                oddsId = odd["oddsId"]
                break
        odds = self.control.odds_get(oddsId)
        results = self.bet.odds_compared(116, odds)
        self.assertIn("SUCCESS", results)

    def test_48_会员投注mmc_重庆秒秒彩_投注(self):
        Pylog.info("TestCase---------------test_48_会员投注mmc_重庆秒秒彩_投注")
        results = self.bet.pre_bet(lotteryId=116)
        self.assertEqual("SUCCESS", results)

    def test_49_会员投注mmc_赛车秒秒彩(self):
        Pylog.info("TestCase---------------test_49_会员投注mmc_赛车秒秒彩")

    def test_50_会员查看投注记录(self):
        Pylog.info("TestCase---------------test_50_会员查看投注记录")
        totalSize = self.memberaction.orderlist_get()
        totalSize = json.loads(totalSize)["data"]["totalSize"]
        Pylog.info("【会员查看投注记录】 注单数：" + str(totalSize))
        self.assertEqual(self.bet.ordertotal, totalSize)

    def test_51_业主查看注单(self):
        Pylog.info("TestCase---------------test_51_业主查看注单")
        totalSize = self.order.order_todaylist(self.membername)
        totalSize = json.loads(totalSize)["data"]["totalSize"]
        Pylog.info("【业主查看注单】 注单数：" + str(totalSize))
        self.assertEqual(self.bet.ordertotal, totalSize)

    def test_52_业主撤单(self):
        Pylog.info("TestCase---------------test_52_业主撤单")
        results = self.order.order_repeal(self.membername)
        self.assertEqual("SUCCESS", results)

    def test_54_csv输出注单信息(self):
        Pylog.info("TestCase---------------test_54_csv输出注单信息")
        orderlist1 = self.order.order_todaylist(self.membername)
        orderlist1 = json.loads(orderlist1)["data"]["rows"]
        orderlist2 = self.order.order_todaylist(memberName=self.membername, lotteryId=10)
        orderlist2 = json.loads(orderlist2)["data"]["rows"]
        orderlist = orderlist1 + orderlist2
        utils.write_csv(orderlist)