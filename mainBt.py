# coding:utf-8
import unittest
import time
from utils.bufReport.BeautifulReport import BeautifulReport
from utils.pylog import Pylog
from config import globalvars
from auth.authors import Authors
from suite.process import regProcess, chgoffProcess, chgonProcess, chgsysProcess, drawProcess, betProcess, cmsProcess, \
    ctconfigProcess

Pylog()
globalvars._init()
pdate = time.strftime("%Y%m%d", time.gmtime())
globalvars.set_value("pdate", pdate)
globalvars.set_value("membername", "lloloj")
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

results = BeautifulReport(suite)
results.report(filename='report', description='Api自动化测试报告', log_path='results/')

