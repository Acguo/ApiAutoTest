# coding:utf-8
import unittest
import time
import json

from auth.authors import Authors
from config import globalvars
from action.memberaction import MemberAction
from action.owner import paramConfig, uaa, payment,content
from utils.pylog import Pylog

class CmsProcess(unittest.TestCase):
    '''cms校验流程'''

    @classmethod
    def setUpClass(cls):
        Pylog.info("***************开始执行用例（CmsProcess）***************")
        cls.auth = Authors(types="member")
        cls.config = globalvars.config()
        cls.paramConfig = paramConfig.ParamConfig()
        cls.content = content.Content()
        cls.memberaction = MemberAction()
        cls.uaa = uaa.Uaa()
        cls.payment = payment.Payment()
        cls.membername = globalvars.get_value("membername")
        owner = cls.config.owner

        #获取图片ID
        actTitlePic = cls.content.upLoadFile('activity.png')
        carouselTitlePic = cls.content.upLoadFile('carousel.png')
        site_iconUrl = cls.content.upLoadFile('H5siteicon.png')
        site_logoUrl = cls.content.upLoadFile('H5sitelogo.png')
        site_h5LogoUrl = cls.content.upLoadFile('H5loginlogo.png')

        #优惠活动参数
        globalvars.set_value("actParam", {"title":"自动化测试","weight":"1","titlePic":actTitlePic,"content":"<p>自动化测试</p>","beginTime":1523894400000,"endTime":1523980799000})
        globalvars.set_value("actTitle", globalvars.get_value("actParam")['title'])
        globalvars.set_value("actTitlePic", globalvars.get_value("actParam")['titlePic'])
        globalvars.set_value("actContent", globalvars.get_value("actParam")['content'])
        globalvars.set_value("actWeight", globalvars.get_value("actParam")['weight'])

        #轮播图参数
        globalvars.set_value("carouselParam", {"beginTime":1523894400000,"delayTime":"1","endTime":1523980799000,"itemPO":[{"link":"http://www.baidu.com","titlePic":carouselTitlePic},{"link":"","titlePic":""}],"title":"自动化测试"})
        globalvars.set_value("carouselTitle", globalvars.get_value("carouselParam")['title'])
        globalvars.set_value("carouselTitlePic", globalvars.get_value("carouselParam")['itemPO'][0]['titlePic'])
        globalvars.set_value("carouselDelayTime", globalvars.get_value("carouselParam")['delayTime'])
        globalvars.set_value("carouselLink", globalvars.get_value("carouselParam")['itemPO'][0]['link'])

        #站点信息参数
        # 查询站点信息
        cls.content.site_view()
        globalvars.set_value("siteParam", {"cid":globalvars.get_value("site_cid"),"platId":owner["env"]["platId"],"iconUrl":site_iconUrl,
                                           "logoUrl":site_logoUrl,"status":1,"h5Name":"自动化测试站点名称","h5SiteUrl":"","h5LogoUrl":site_h5LogoUrl})
        globalvars.set_value("site_h5Name", globalvars.get_value("siteParam")['h5Name'])
        globalvars.set_value("site_iconUrl", site_iconUrl)
        globalvars.set_value("site_logoUrl", site_logoUrl)
        globalvars.set_value("site_h5LogoUrl", site_h5LogoUrl)

    @classmethod
    def tearDownClass(cls):
        Pylog.info("***************结束执行用例（CmsProcess）***************")

    def test_01_业主彩种排序设定(self):
        Pylog.info("TestCase---------------test_01_业主彩种排序设定")
        # 查询彩种排序信息
        tmp = self.paramConfig.lotteryWeight_list()
        self.assertIsNotNone(tmp)
        json_dict = json.loads(tmp)
        param = json_dict['data']['rows'][0]
        # 保存查询到的信息
        globalvars.set_value("aliasName", json_dict['data']['rows'][0]['aliasName'])
        globalvars.set_value("weight", json_dict['data']['rows'][0]['weight'])
        globalvars.set_value("imgUrl", json_dict['data']['rows'][0]['imgUrl'])
        # 设置“展示名称”、“权重”、“彩种图标”
        results = self.paramConfig.lotteryWeight_save(param)
        # 断言
        self.assertIn("SUCCESS", results)

    def test_02_业主客服设定(self):
        Pylog.info("TestCase---------------test_02_业主客服设定")
        # 查询客服地址
        tmp = self.paramConfig.custConfig_view()
        self.assertIsNotNone(tmp)
        json_dict = json.loads(tmp)
        param = json_dict['data']
        # 保存查询到的客服地址
        globalvars.set_value("h5CustUrl", json_dict['data']['h5CustUrl'])
        # 设置客服地址
        results = self.paramConfig.custConfig_save(param)
        # 断言
        self.assertIn("SUCCESS", results)

    def test_03_业主app地址设定(self):
        Pylog.info("TestCase---------------test_03_业主app地址设定")
        # 查询app地址
        tmp = self.paramConfig.appConfig_view()
        self.assertIsNotNone(tmp)
        json_dict = json.loads(tmp)
        param = json_dict['data']
        # 保存查询到的app地址
        globalvars.set_value("appUrl", json_dict['data']['url'])
        # 设置app地址
        results = self.paramConfig.appConfig_save(param)
        # 断言
        self.assertIn("SUCCESS", results)

    def test_04_业主站点信息设定(self):
        Pylog.info("TestCase---------------test_04_业主站点信息设定")
        # 设置站点信息
        param = globalvars.get_value("siteParam")
        results = self.content.site_save(param)
        # 断言
        self.assertIn("SUCCESS", results)

    def test_05_业主新手教程设定(self):
        Pylog.info("TestCase---------------test_05_业主新手教程设定")
        # 查询新手教程
        tmp = self.content.copyright_list(type=1)
        self.assertIsNotNone(tmp)
        json_dict = json.loads(tmp)
        param = json_dict['data']['rows'][0]
        param['title'] = "自动化测试"
        param['content'] = "自动化测试"
        # 保存查询到的新手教程
        globalvars.set_value("BT01title", param['title'])
        globalvars.set_value("BT01content", param['content'])
        globalvars.set_value("BT01status", param['status'])
        # 设置新手教程
        results = self.content.copyright_save(param)
        # 断言
        self.assertIn("SUCCESS", results)

    def test_06_业主代理加盟设定(self):
        Pylog.info("TestCase---------------test_06_业主代理加盟设定")
        # 查询代理加盟
        tmp = self.content.copyright_list(type=1)
        self.assertIsNotNone(tmp)
        json_dict = json.loads(tmp)
        param = json_dict['data']['rows'][1]
        param['title'] = "自动化测试"
        param['content'] = "自动化测试"
        # 保存查询到的代理加盟
        globalvars.set_value("BT02title", param['title'])
        globalvars.set_value("BT02content", param['content'])
        globalvars.set_value("BT02status", param['status'])
        # 设置代理加盟
        results = self.content.copyright_save(param)
        # 断言
        self.assertIn("SUCCESS", results)

    def test_07_业主关于我们设定(self):
        Pylog.info("TestCase---------------test_07_业主关于我们设定")
        # 查询关于我们
        tmp = self.content.copyright_list(type=1)
        self.assertIsNotNone(tmp)
        json_dict = json.loads(tmp)
        param = json_dict['data']['rows'][3]
        param['title'] = "自动化测试"
        param['content'] = "自动化测试"
        # 保存查询到的关于我们
        globalvars.set_value("BT04title", param['title'])
        globalvars.set_value("BT04content", param['content'])
        globalvars.set_value("BT04status", param['status'])
        # 设置关于我们
        results = self.content.copyright_save(param)
        # 断言
        self.assertIn("SUCCESS", results)

    def test_08_业主充值教程设定(self):
        Pylog.info("TestCase---------------test_08_业主充值教程设定")
        # 查询充值教程
        tmp = self.content.copyright_list(type=1)
        self.assertIsNotNone(tmp)
        json_dict = json.loads(tmp)
        param = json_dict['data']['rows'][4]
        param['title'] = "自动化测试"
        param['content'] = "自动化测试"
        # 保存查询到的充值教程
        globalvars.set_value("BT05title", param['title'])
        globalvars.set_value("BT05content", param['content'])
        globalvars.set_value("BT05status", param['status'])
        # 设置充值教程
        results = self.content.copyright_save(param)
        # 断言
        self.assertIn("SUCCESS", results)

    def test_09_业主注册说明设定(self):
        Pylog.info("TestCase---------------test_09_业主注册说明设定")
        # 查询注册说明
        tmp = self.content.copyright_list(type=2)
        self.assertIsNotNone(tmp)
        json_dict = json.loads(tmp)
        param = json_dict['data']['rows'][0]
        param['title'] = "自动化测试"
        param['content'] = "自动化测试"
        # 保存查询到的注册说明
        globalvars.set_value("ZT03title", param['title'])
        globalvars.set_value("ZT03content", param['content'])
        globalvars.set_value("ZT03status", param['status'])
        # 设置注册说明
        results = self.content.copyright_save(param)
        # 断言
        self.assertIn("SUCCESS", results)

    def test_10_业主存款弹窗设定(self):
        Pylog.info("TestCase---------------test_10_业主存款弹窗设定")
        # 查询存款弹窗
        tmp = self.content.copyright_list(type=3)
        self.assertIsNotNone(tmp)
        json_dict = json.loads(tmp)
        param = json_dict['data']['rows'][0]
        param['title'] = "自动化测试"
        param['content'] = "自动化测试"
        # 保存查询到的存款弹窗
        globalvars.set_value("AT01title", param['title'])
        globalvars.set_value("AT01content", param['content'])
        globalvars.set_value("AT01status", param['status'])
        # 设置存款弹窗
        results = self.content.copyright_save(param)
        # 断言
        self.assertIn("SUCCESS", results)

    def test_11_业主支付宝钱包设定(self):
        Pylog.info("TestCase---------------test_11_业主支付宝钱包设定")
        # 查询支付宝钱包
        tmp = self.content.copyright_list(type=3)
        self.assertIsNotNone(tmp)
        json_dict = json.loads(tmp)
        param = json_dict['data']['rows'][1]
        param['title'] = "自动化测试"
        param['content'] = "自动化测试"
        # 保存查询到的支付宝钱包
        globalvars.set_value("AT02title", param['title'])
        globalvars.set_value("AT02content", param['content'])
        globalvars.set_value("AT02status", param['status'])
        # 设置支付宝钱包
        results = self.content.copyright_save(param)
        # 断言
        self.assertIn("SUCCESS", results)

    def test_12_业主微信钱包设定(self):
        Pylog.info("TestCase---------------test_12_业主微信钱包设定")
        # 查询微信钱包
        tmp = self.content.copyright_list(type=3)
        self.assertIsNotNone(tmp)
        json_dict = json.loads(tmp)
        param = json_dict['data']['rows'][2]
        param['title'] = "自动化测试"
        param['content'] = "自动化测试"
        # 保存查询到的微信钱包
        globalvars.set_value("AT03title", param['title'])
        globalvars.set_value("AT03content", param['content'])
        globalvars.set_value("AT03status", param['status'])
        # 设置微信钱包
        results = self.content.copyright_save(param)
        # 断言
        self.assertIn("SUCCESS", results)

    def test_13_业主优惠活动列表设定_全部删除(self):
        Pylog.info("TestCase---------------test_13_业主优惠活动列表设定_全部删除")
        results = self.content.activity_deleteAll()
        self.assertIn("SUCCESS", results)

    def test_14_业主优惠活动列表设定_新增(self):
        Pylog.info("TestCase---------------test_14_业主优惠活动列表设定_新增")
        results = self.content.activity_create(param =globalvars.get_value("actParam"))
        self.assertIn("SUCCESS", results)

    def test_15_业主轮播图设定_全部删除(self):
        Pylog.info("TestCase---------------test_15_业主轮播图设定_全部删除")
        results = self.content.carousel_deleteAll()
        self.assertIn("SUCCESS", results)

    def test_16_业主轮播图设定_新增(self):
        Pylog.info("TestCase---------------test_16_业主轮播图设定_新增")
        param = globalvars.get_value("carouselParam")
        param['title'] = '自动化测试'
        results = self.content.carousel_create(param = param)
        self.assertIn("SUCCESS", results)

    def test_17_业主公告设定_全部删除(self):
        Pylog.info("TestCase---------------test_17_业主公告设定_全部删除")
        results = self.content.notice_deleteAll()
        self.assertIn("SUCCESS", results)

    def test_18_业主公告设定_新增(self):
        Pylog.info("TestCase---------------test_18_业主公告设定_新增")
        results = self.content.notice_create(datas="自动化测试公告内容")
        self.assertIn("SUCCESS", results)

    def test_19_业主首页弹屏设定_全部删除(self):
        Pylog.info("TestCase---------------test_19_业主首页弹屏设定_全部删除")
        results = self.content.popText_deleteAll()
        self.assertIn("SUCCESS", results)

    def test_20_业主首页弹屏设定_新增(self):
        Pylog.info("TestCase---------------test_20_业主首页弹屏设定_新增")
        results = self.content.popText_create(datas="自动化测试首页弹屏内容")
        self.assertIn("SUCCESS", results)

    def test_21_业主站内信设定_全部删除(self):
        Pylog.info("TestCase---------------test_21_业主站内信设定_全部删除")

    def test_22_业主站内信设定_新增(self):
        Pylog.info("TestCase---------------test_22_业主站内信设定_新增")
        results = self.content.instationMsg_save(content="测试数据test data！！")
        self.assertIn("SUCCESS", results)

    def test_23_彩种排序验证(self):
        Pylog.info("TestCase---------------test_23_彩种排序验证")
        #获取彩种排序
        tmp = self.memberaction.apid_lotterys()
        json_dict = json.loads(tmp)
        #获取“展示名称”
        name = json_dict['data'][0]['name']
        # 获取“权重”
        orderCount = json_dict['data'][0]['orderCount']
        # 获取“彩种图标”
        imgUrl = json_dict['data'][0]['imgUrl']
        #断言
        self.assertEqual(name, globalvars.get_value("aliasName"))
        self.assertEqual(orderCount, globalvars.get_value("weight"))
        self.assertEqual(imgUrl, globalvars.get_value("imgUrl"))

    def test_24_客服设定验证(self):
        Pylog.info("TestCase---------------test_24_客服设定验证")
        #获取客服地址
        tmp = self.memberaction.config_custConfig()
        json_dict = json.loads(tmp)
        h5CustUrl = json_dict['data']['h5CustUrl']
        #断言
        self.assertEqual(h5CustUrl, globalvars.get_value("h5CustUrl"))

    def test_25_app地址设定验证(self):
        Pylog.info("TestCase---------------test_25_app地址设定验证")
        #获取app地址
        tmp = self.memberaction.config_appConfig()
        json_dict = json.loads(tmp)
        url = json_dict['data']['url']
        #断言
        self.assertEqual(url, globalvars.get_value("appUrl"))

    def test_26_站点信息设定验证(self):
        Pylog.info("TestCase---------------test_26_站点信息设定验证")
        #获取站点信息
        tmp = self.memberaction.cms_site()
        json_dict = json.loads(tmp)
        #获取“H5站点名称”
        h5Name = json_dict['data']['h5Name']
        # 获取“H5站点页签icon”
        iconUrl = json_dict['data']['iconUrl']
        # 获取“H5站点logo”
        logoUrl = json_dict['data']['logoUrl']
        # 获取“H5站点登录页logo”
        h5LogoUrl = json_dict['data']['h5LogoUrl']
        #断言
        self.assertEqual(h5Name, globalvars.get_value("site_h5Name"))
        self.assertEqual(iconUrl, globalvars.get_value("site_iconUrl"))
        self.assertEqual(logoUrl, globalvars.get_value("site_logoUrl"))
        self.assertEqual(h5LogoUrl, globalvars.get_value("site_h5LogoUrl"))

    def test_27_新手教程设定验证(self):
        Pylog.info("TestCase---------------test_27_新手教程设定验证")
        #获取新手教程
        tmp = self.memberaction.cms_copyright(type=1, code='BT01')
        json_dict = json.loads(tmp)
        #如果是停用状态的话data为空
        if globalvars.get_value("BT01status") == 0:
            self.assertIsNone(json_dict['data'])
        #如果是启用状态的话取data里面的标题和内容进行判断
        else:
            #获取“新手教程”标题
            title = json_dict['data'][0]['title']
            #获取“新手教程”内容
            content = json_dict['data'][0]['content']
            #断言
            self.assertEqual(title, globalvars.get_value("BT01title"))
            self.assertEqual(content, globalvars.get_value("BT01content"))

    def test_28_代理加盟设定验证(self):
        Pylog.info("TestCase---------------test_28_代理加盟设定验证")
        #获取代理加盟
        tmp = self.memberaction.cms_copyright(type=1, code='BT02')
        json_dict = json.loads(tmp)
        #如果是停用状态的话data为空
        if globalvars.get_value("BT02status") == 0:
            self.assertIsNone(json_dict['data'])
        #如果是启用状态的话取data里面的标题和内容进行判断
        else:
            #获取“代理加盟”标题
            title = json_dict['data'][0]['title']
            #获取“代理加盟”内容
            content = json_dict['data'][0]['content']
            #断言
            self.assertEqual(title, globalvars.get_value("BT02title"))
            self.assertEqual(content, globalvars.get_value("BT02content"))

    def test_29_关于我们设定验证(self):
        Pylog.info("TestCase---------------test_29_关于我们设定验证")
        #获取关于我们
        tmp = self.memberaction.cms_copyright(type=1, code='BT04')
        json_dict = json.loads(tmp)
        #如果是停用状态的话data为空
        if globalvars.get_value("BT04status") == 0:
            self.assertIsNone(json_dict['data'])
        #如果是启用状态的话取data里面的标题和内容进行判断
        else:
            #获取“关于我们”标题
            title = json_dict['data'][0]['title']
            #获取“关于我们”内容
            content = json_dict['data'][0]['content']
            #断言
            self.assertEqual(title, globalvars.get_value("BT04title"))
            self.assertEqual(content, globalvars.get_value("BT04content"))

    def test_30_充值教程设定验证(self):
        Pylog.info("TestCase---------------test_30_充值教程设定验证")
        #获取充值教程
        tmp = self.memberaction.cms_copyright(type=1, code='BT05')
        json_dict = json.loads(tmp)
        #如果是停用状态的话data为空
        if globalvars.get_value("BT05status") == 0:
            self.assertIsNone(json_dict['data'])
        #如果是启用状态的话取data里面的标题和内容进行判断
        else:
            #获取“充值教程”标题
            title = json_dict['data'][0]['title']
            #获取“充值教程”内容
            content = json_dict['data'][0]['content']
            #断言
            self.assertEqual(title, globalvars.get_value("BT05title"))
            self.assertEqual(content, globalvars.get_value("BT05content"))

    def test_31_注册说明设定验证(self):
        Pylog.info("TestCase---------------test_31_注册说明设定验证")
        #获取注册说明
        tmp = self.memberaction.cms_copyright(type=2, code='ZT03')
        json_dict = json.loads(tmp)
        #如果是停用状态的话data为空
        if globalvars.get_value("ZT03status") == 0:
            self.assertIsNone(json_dict['data'])
        #如果是启用状态的话取data里面的标题和内容进行判断
        else:
            #获取“注册说明”标题
            title = json_dict['data'][0]['title']
            #获取“注册说明”内容
            content = json_dict['data'][0]['content']
            #断言
            self.assertEqual(title, globalvars.get_value("ZT03title"))
            self.assertEqual(content, globalvars.get_value("ZT03content"))

    def test_32_存款弹窗设定验证(self):
        Pylog.info("TestCase---------------test_32_存款弹窗设定验证")
        #获取存款弹窗
        tmp = self.memberaction.cms_copyright(type=3, code='AT01')
        json_dict = json.loads(tmp)
        #如果是停用状态的话data为空
        if globalvars.get_value("AT01status") == 0:
            self.assertIsNone(json_dict['data'])
        #如果是启用状态的话取data里面的标题和内容进行判断
        else:
            #获取“存款弹窗”标题
            title = json_dict['data'][0]['title']
            #获取“存款弹窗”内容
            content = json_dict['data'][0]['content']
            #断言
            self.assertEqual(title, globalvars.get_value("AT01title"))
            self.assertEqual(content, globalvars.get_value("AT01content"))

    def test_33_支付宝钱包设定验证(self):
        Pylog.info("TestCase---------------test_33_支付宝钱包设定验证")
        #获取支付宝钱包
        tmp = self.memberaction.cms_copyright(type=3, code='AT02')
        json_dict = json.loads(tmp)
        #如果是停用状态的话data为空
        if globalvars.get_value("AT02status") == 0:
            self.assertIsNone(json_dict['data'])
        #如果是启用状态的话取data里面的标题和内容进行判断
        else:
            #获取“支付宝钱包”标题
            title = json_dict['data'][0]['title']
            #获取“支付宝钱包”内容
            content = json_dict['data'][0]['content']
            #断言
            self.assertEqual(title, globalvars.get_value("AT02title"))
            self.assertEqual(content, globalvars.get_value("AT02content"))

    def test_34_微信钱包设定验证(self):
        Pylog.info("TestCase---------------test_34_微信钱包设定验证")
        #获取支付宝钱包
        tmp = self.memberaction.cms_copyright(type=3, code='AT03')
        json_dict = json.loads(tmp)
        #如果是停用状态的话data为空
        if globalvars.get_value("AT03status") == 0:
            self.assertIsNone(json_dict['data'])
        #如果是启用状态的话取data里面的标题和内容进行判断
        else:
            #获取“支付宝钱包”标题
            title = json_dict['data'][0]['title']
            #获取“支付宝钱包”内容
            content = json_dict['data'][0]['content']
            #断言
            self.assertEqual(title, globalvars.get_value("AT03title"))
            self.assertEqual(content, globalvars.get_value("AT03content"))

    def test_35_优惠活动列表设定验证(self):
        Pylog.info("TestCase---------------test_35_优惠活动列表设定验证")
        #获取优惠活动
        tmp = self.memberaction.cms_activityInfo(cid=globalvars.get_value("actCid"))
        json_dict = json.loads(tmp)
        #获取“优惠活动标题”
        title = json_dict['data']['title']
        # 获取“优惠活动图片”
        titlePic = json_dict['data']['titlePic']
        # 获取“优惠活动内容”
        content = json_dict['data']['content']
        # 获取“优惠活动权重”
        weight = str(json_dict['data']['weight'])
        #断言
        self.assertEqual(title, globalvars.get_value("actTitle"))
        self.assertEqual(titlePic, globalvars.get_value("actTitlePic"))
        self.assertEqual(content, globalvars.get_value("actContent"))
        self.assertEqual(weight, globalvars.get_value("actWeight"))

    def test_36_轮播图设定验证(self):
        Pylog.info("TestCase---------------test_36_轮播图设定验证")
        #获取轮播图
        tmp = self.memberaction.cms_carousel()
        json_dict = json.loads(tmp)
        #获取“轮播图标题”
        title = json_dict['data']['title']
        # 获取“轮播图图片”
        titlePic = json_dict['data']['itemPO'][0]['titlePic']
        # 获取“轮播图链接”
        link = json_dict['data']['itemPO'][0]['link']
        # 获取“轮播图延迟时间”
        delayTime = str(json_dict['data']['delayTime'])
        #断言
        self.assertEqual(title, globalvars.get_value("carouselTitle"))
        self.assertEqual(titlePic, globalvars.get_value("carouselTitlePic"))
        self.assertEqual(link, globalvars.get_value("carouselLink"))
        self.assertEqual(delayTime, globalvars.get_value("carouselDelayTime"))

    def test_37_公告设定验证(self):
        Pylog.info("TestCase---------------test_37_公告设定验证")
        #获取公告
        tmp = self.memberaction.cms_notice()
        json_dict = json.loads(tmp)
        #获取“公告标题”
        title = json_dict['data'][0]['title']
        # 获取“公告权重”
        weight = json_dict['data'][0]['weight']
        # 获取“公告内容”
        content = json_dict['data'][0]['content']
        #断言
        self.assertEqual(title, globalvars.get_value("noticeTitle"))
        self.assertEqual(weight, globalvars.get_value("noticeWeight"))
        self.assertEqual(content, globalvars.get_value("noticeContent"))

    def test_38_首页弹屏验证(self):
        Pylog.info("TestCase---------------test_38_首页弹屏验证")
        #获取首页弹屏
        tmp = self.memberaction.cms_popText()
        json_dict = json.loads(tmp)
        #获取“首页弹屏标题”
        title = json_dict['data'][0]['title']
        # 获取“首页弹屏内容”
        content = json_dict['data'][0]['content']
        #断言
        self.assertEqual(title, globalvars.get_value("popTextTitle"))
        self.assertEqual(content, globalvars.get_value("popTextContent"))

    def test_39_站内信设定验证(self):
        Pylog.info("TestCase---------------test_39_站内信设定验证")
        #获取站内信
        tmp = self.memberaction.msg_list()
        json_dict = json.loads(tmp)
        #获取“站内信标题”
        title = json_dict['data']['data']['rows'][0]['title']
        # 获取“站内信内容”
        content = json_dict['data']['data']['rows'][0]['content']
        #断言
        self.assertEqual(title, globalvars.get_value("msgTitle"))
        self.assertEqual(content, globalvars.get_value("msgContent"))

if __name__ == "__main__":
    Pylog()
    testsuite = unittest.makeSuite(CmsProcess)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(testsuite)



