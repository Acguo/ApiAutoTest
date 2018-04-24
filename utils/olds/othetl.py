# coding:utf-8
import requests
from auth.authors import Authors


def discount():
    auth = Authors(types="control")
    headers = auth.headers

    datas = {"startTime": "1517760000000", "endTime": "1518364799000", "platAccount": "xq_double"}
    url = "http://" + auth.config.owner["control"]["host"] + "/arespayment/apis/master/money/statistics/discount/owner"
    resp = requests.get(url=url, headers=headers, params=datas)
    return resp.text


def offline():
    auth = Authors(types="control")
    headers = auth.headers
    datas = {"page": 1, "rows": 15, "start": "1517760000000",
             "ende": "1518364799000", "account": "xq_double"}
    url = "http://" + auth.config.owner["control"]["host"] + "/arespayment/apis/report/offline"
    resp = requests.get(url=url, headers=headers, params=datas)
    return resp.text


def offline_detail():
    auth = Authors(types="control")
    headers = auth.headers
    datas = {"page": 1, "rows": 15, "start": "1517760000000",
             "ende": "1518364799000", "id": 38, "account": None, "rule": None, "orderId": None}
    url = "http://" + auth.config.owner["control"]["host"] + "/arespayment/apis/report/offline/detail"
    resp = requests.get(url=url, headers=headers, params=datas)
    return resp.text


def online():
    auth = Authors(types="control")
    headers = auth.headers
    datas = {"page": 1, "rows": 15, "start": "1517760000000",
             "ende": "1518364799000", "account": ""}
    url = "http://" + auth.config.owner["control"]["host"] + "/arespayment/apis/report/online"
    resp = requests.get(url=url, headers=headers, params=datas)
    return resp.text


def online_detail():
    auth = Authors(types="control")
    headers = auth.headers
    datas = {"page": 1, "rows": 15, "start": "1517760000000",
             "ende": "1518364799000", "id": 38, "account": None, "rule": None, "orderId": None}
    url = "http://" + auth.config.owner["control"]["host"] + "/arespayment/apis/report/online/detail"
    resp = requests.get(url=url, headers=headers, params=datas)
    return resp.text


def manul_prize():
    auth = Authors(types="control")
    headers = auth.headers
    url = "http://192.168.0.223:8080/venus/apis/lottery/draw/prize"
    datas = {
        "pcode": "2018038",
        "code": "xg_lhc",
        "lotteryCId": "10",
        "drawPrizeStatus": "",
    }
    resp = requests.post(url=url, headers=headers, params=datas)
    return resp.text




print(manul_prize())
