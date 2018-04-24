# coding:utf-8

import json
import requests
from utils.pylog import Pylog
from auth.authors import Authors
from config import globalvars


def get_random(lottery=10, playid=None):
    '''
    :param lottery: 彩种ID
    :param playid: 玩法ID
    :return: 所有玩法及内容
    '''
    config = globalvars.config()
    if globalvars.get_value("headers_control") is None:
        Authors(types="control")

    headers = globalvars.get_value("headers_control")
    url_get = "http://{}{}".format(config.owner["control"]["host"], config.api["control"]["getplays"])
    resp = requests.get(url=url_get, params={"lotteryId": lottery, "playId": playid},
                        headers=headers, timeout=5)
    Pylog.debug("【随机注单-resp】" + resp.text)
    datas = json.loads(resp.text)["data"]
    # Pylog.info("【获取api投注数量(lotteryId:{})】：".format(lottery) + str(len(datas)))
    return datas

if __name__ == "__main__":
    globalvars._init()
    print(get_random(lottery=2))