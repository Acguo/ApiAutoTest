import csv
import json
import requests
from auth.authors import Authors
from config import globalvars
from utils import utils
'''
    方案列表导出
'''



def write_csv(data):
    paths = utils.findPath()
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
    globalvars._init()
    Authors()
    host = globalvars.config().owner["env"]["host_yz"]
    url = "http://" + host + "/hermes/apis/plat/order/management/today/list"
    memberName = "1314520wws"
    headers = globalvars.get_value("headers_owner")
    datas = {"memberName": memberName, "orderId": None,
             "condition": json.dumps(
                 {"sideType": "2", "page": 1, "count": 1000, "betStartTime": None, "betEndTime": None,
                  "memberName": memberName,
                  "orderId": "", "status": "", "playId": "", "agent": ""})
             }
    datas_xglhc = {"memberName": memberName, "orderId": None,
                   "condition": json.dumps(
                       {"sideType": "2", "page": 1, "count": 1000, "betStartTime": None, "betEndTime": None,
                        "memberName": memberName,
                        "orderId": "", "status": "", "playId": "", "agent": "", "lotteryId": 10})
                   }

    resp = requests.get(url=url, headers=headers, params=datas)
    resp2 = requests.get(url=url, headers=headers, params=datas_xglhc)
    datas = json.loads(resp.text)["data"]["rows"] + json.loads(resp2.text)["data"]["rows"]
    print(len(datas))
    write_csv(datas)
