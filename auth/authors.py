# -*- coding:utf-8 -*-
import requests
import json

from utils.pylog import Pylog
from config import globalvars


class Authors():
    def __init__(self, types="owner"):
        config = globalvars.config()
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "clientId": "BH80xYtfSel9Yr2p_1uQKi8N7Fg8mBVhlCqJROWL",
            "Authorization": "Basic d2ViX2FwcDo="
        }

        control_host = config.owner["env"]["host_ct"]
        control_api_login = config.api["control"]["login"]
        control_origin = config.owner["env"]["origin_ct"]
        control_model_login = config.model("control", "login.json")

        owner_origin = config.owner["env"]["origin_yz"]
        owner_host = config.owner["env"]["host_yz"]
        owner_api_login = config.api["owner"]["login"]
        owner_model_login = config.model("owner", "login.json")

        member_orgin = config.owner["env"]["origin_mb"]
        member_host = config.owner["env"]["host_mb"]
        member_api_login = config.api["member"]["login"]
        member_model_login = config.model("member", "login.json")

        if types == "control":
            url_login = "http://" + control_host + control_api_login
            control_model_login["username"] = "victor"
            headers.update({"Origin": control_origin})
            Pylog.info(
                "【登陆鉴权" + types + "】 | " + control_model_login["username"] + " " + control_model_login["password"])
            resp = requests.post(url=url_login,
                                 params=control_model_login,
                                 headers=headers,
                                 timeout = 5)
            Pylog.debug(resp.text)
            globalvars.set_value("headers_control", headers)

        elif types == "owner":
            url_login = "http://" + owner_host + owner_api_login
            owner_model_login["username"] = "victor"
            headers.update({"Origin": owner_origin})
            Pylog.info("【登陆鉴权" + types + "】 | " + owner_model_login["username"] + " " + owner_model_login["password"])
            resp = requests.post(url=url_login,
                                 params=owner_model_login,
                                 headers=headers,
                                 timeout=5)
            Pylog.debug(resp.text)
            globalvars.set_value("headers_owner", headers)

        else:
            url_login = "http://" + member_host + member_api_login
            member_model_login["username"] = "vctscript"
            headers.update({"Content-Type": "application/x-www-form-urlencoded",
                            "Origin": member_orgin})
            Pylog.info("【登陆鉴权" + types + "】 | " + member_model_login["username"] + " " + member_model_login["password"])
            resp = requests.post(url=url_login,
                                 data=member_model_login,
                                 headers=headers,
                                 timeout=5)
            Pylog.debug(resp.text)
            globalvars.set_value("headers_member", headers)
        try:
            resp = json.loads(resp.content)["data"]
            Pylog.debug("【获取token】：" + resp["token_type"] + " " + resp["access_token"])
            headers["Authorization"] = str(resp["token_type"]) + " " + str(resp["access_token"])
        except Exception:
            Pylog.error("【登陆错误】：" + Pylog.exinfo())
        headers["Content-Type"] = 'application/json; charset=UTF-8'


if __name__ == "__main__":
    Pylog()
    globalvars._init()
    Authors("owner")
    Authors("member")
    Authors("control")
