# coding:utf-8

from utils.pylog import Pylog
from utils import utils
import json


class Config:
    def __init__(self):

        self.__path = utils.findPath()+"config\\{}"
        with open(self.__path.format("apis\\api_config.json"), encoding="utf-8") as files:
            datas = json.load(files)
            self.api = datas


        with open(self.__path.format("envinfo\\owner_config.json"), encoding="utf-8") as files:
            datas = json.load(files)
            self.owner = {}
            self.owner["env"] = datas[datas["env"]]
            self.owner["control"] = datas["control"]

    def model(self, role=None, filename=None):
        try:
            if role is None:
                with open(self.__path.format("models\\" + filename), encoding="utf-8") as files:
                    datas = json.load(files)
            else:
                with open(self.__path.format("models\\" + role + "\\" + filename), encoding="utf-8") as files:
                    datas = json.load(files)
            return datas
        except Exception:
            Pylog.error("【打开json文件错误】：" + Pylog.exinfo())


if __name__ == "__main__":
    results = Config()
    print(results.model(role="member", filename="lotteryId.json"))