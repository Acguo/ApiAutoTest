# coding:utf-8
import time
import csv
import os
import platform


def datetime_timestamp(dt):
    '''时间戳转换工具'''
    # dt为字符串
    # tuiyong(datetime_timestamp('2018-01-30 00:00:00') * 1000,
    #         datetime_timestamp('2018-01-30 23:59:59') * 1000)
    # 中间过程，一般都需要将字符串转化为时间数组
    time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    return int(s)


def findPath(files="main.py"):
    '''获取工程目录'''
    o_path = os.getcwd()
    if 'Windows' in platform.system():
        separator = '\\'
    else:
        separator = '/'
    str = o_path
    str = str.split(separator)
    while len(str) > 0:
        spath = separator.join(str) + separator + files
        leng = len(str)
        if os.path.exists(spath):
            return spath.replace(files, "")
        str.remove(str[leng - 1])


def playsTreeRecursive(plays, odddict):
    '''会员玩法树递归'''

    for odds in plays:
        if "childrens" in list(odds.keys()):
            playsTreeRecursive(odds["childrens"], odddict)
        else:
            if "playId" in odds["oddsData"]:
                playId = odds["oddsData"]["playId"]
                payoff = odds["oddsData"]["payoff"]
            else:
                continue
            odddict[playId] = payoff
    return odddict

def write_csv(data):
    paths = findPath()
    cscfile = open(paths + '\\results\\ordercsvfile.csv', 'w', newline='')
    writer2 = csv.writer(cscfile)
    writer2.writerow(["彩种", "期数", "方案ID", "玩法Name", "玩法Id", "下注内容", "投注金额", "开奖号码", "结果", "派彩", "返点"])
    for item in data:
        item["winNumber"] = item["winNumber"] if "winNumber" in item.keys() else ''
        item["playName"] = item["playName"] if "playName" in item.keys() else ''
        writer2.writerow([item["lotteryName"], item["pcode"], item["orderId"], item["playName"], item["playId"],
                          item["betContent"], str(int(item["betAmount"]) / 100), item["winNumber"],
                          item["orderStatusString"], str(int(item["payoff"]) / 100),
                          str(int(item["reforwardPoint"]) / 100)])
    cscfile.close()



if __name__ == "__main__":
    pass