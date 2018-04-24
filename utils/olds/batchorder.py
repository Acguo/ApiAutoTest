# coding:utf-8
import json
import requests
from auth.authors import Authors
from config import globalvars
'''
    算法测试
'''

class BatchOrder():
    def get_betrandom(self, lottery, playid=None):
        '''get随机玩法参数'''
        config = globalvars.config()
        Authors(types="control")
        headers = globalvars.get_value("headers_control")

        url_get = "http://{}{}".format(config.owner["control"]["host"], config.api["control"]["getplays"])
        resp = requests.get(url=url_get, params={"lotteryId": lottery, "playId": playid}, headers=headers)
        datas = json.loads(resp.text)["data"]
        for k, v in datas.items():
            dicts = {}
            dicts["play_id"] = k.split("|")[0]
            dicts["play_name"] = k.split("|")[1]
            dicts["content"] = v.split("|")[1]
            dicts["count"] = v.split("|")[0]
            #http://192.168.0.221:8081    http://121.58.234.210:8081  http://192.168.0.220:8081
            url_x = "http://192.168.0.220:8081/api_test/batchOrder/export"
            data_x = {"lotteryId": lottery,
                      "playId": dicts["play_id"],
                      "betCount": "5000",
                      "betContent": dicts["content"]}
            filename = open("./{}.csv".format(str(dicts["play_id"])+"_"+dicts["play_name"]), "w")
            for i in range(0, 20):
                resp = requests.get(url=url_x, params=data_x)
                csvs = resp.text
                lists = csvs.split("\n")
                if i == 0:
                    csvs = csvs.replace(lists[-2]+"\n", "")
                else:
                    csvs = csvs.replace(lists[0] + "\n", "")
                    csvs = csvs.replace(lists[-2] + "\n", "")
                filename.write(csvs)
            filename.close()
            print("**********" + dicts["play_name"] + "**********")
        print(len(datas))


if __name__ == "__main__":
    globalvars._init()
    BatchOrder().get_betrandom(2,22201)
