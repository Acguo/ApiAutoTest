# coding:utf-8
import unittest
import time
import sys
import xmlrunner
from utils import HTMLTestReportCN
from utils.pylog import Pylog
from config import globalvars
from auth.authors import Authors
from suite.process import regProcess, chgoffProcess, chgonProcess, chgsysProcess, drawProcess, betProcess, cmsProcess, \
    ctconfigProcess

params = sys.argv
globalvars._init()
if len(params) > 1:
    globalvars.set_value("membername", params[1])
# globalvars.set_value("membername", "ddee3")
Pylog()
pdate = time.strftime("%Y%m%d", time.gmtime())
globalvars.set_value("pdate", pdate)
Authors("owner")
Authors("control")

suite = unittest.TestSuite()
# suite.addTest(unittest.makeSuite(regProcess.RegProcess))
# suite.addTest(unittest.makeSuite(chgoffProcess.ChgoffProcess))
# suite.addTest(unittest.makeSuite(chgonProcess.ChgonProcess))
# suite.addTest(unittest.makeSuite(chgsysProcess.ChgsysProcess))
# suite.addTest(unittest.makeSuite(drawProcess.DrawProcess))
# suite.addTest(unittest.makeSuite(ctconfigProcess.CtconfigProcess))
# suite.addTest(unittest.makeSuite(betProcess.BetProcess))
suite.addTest(unittest.makeSuite(cmsProcess.CmsProcess))

filename = 'results/report.html'
fp = open(filename, 'wb')
runner = HTMLTestReportCN.HTMLTestRunner(
    stream=fp,
    title=u'测试报告',
    description=u'用例的执行情况')


runner.run(suite)
fp.close()
