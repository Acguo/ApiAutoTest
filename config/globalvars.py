# coding: utf-8
from config import configutil


def _init():
    '''初始化'''
    global _global_dict
    global _configs

    _global_dict = {}
    _global_dict["username"] = "vctscript"
    _global_dict["headers"] = {}
    _configs = configutil.Config()


def set_value(key, value):
    '''定义一个全局变量'''
    _global_dict[key] = value


def get_value(key, defValue=None):
    '''获取全局变量'''
    try:
        return _global_dict[key]
    except KeyError:
        return defValue


def config():
    '''返回配置对象'''
    return _configs
