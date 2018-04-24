# -*- coding: UTF-8 -*-
import logging
import os
import platform
import traceback


class Pylog:
    def __init__(self):

        # 获取相对路径
        paths = ""
        o_path = os.getcwd()
        if 'Windows' in platform.system():
            separator = '\\'
        else:
            separator = '/'
        str = o_path
        str = str.split(separator)
        while len(str) > 0:
            spath = separator.join(str) + separator + "main.py"
            leng = len(str)
            if os.path.exists(spath):
                paths = spath.replace("main.py", "")
            str.remove(str[leng - 1])

        ##############################日志配置############################################################
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename=paths + "\\results\\log.txt",
                            filemode='w'
                            )
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        ###################################################################################################

    @staticmethod
    def info(data=None):
        # logging.info(Colors(data,"black"))
        logging.info(data)

    @staticmethod
    def debug(data=None):
        logging.debug(data)
        # logging.debug(Colors(data,"blue"))

    @staticmethod
    def error(data=None):
        logging.error(data)
        # logging.error(Colors(data,"red"))

    @staticmethod
    def warning(data=None):
        logging.warning(data)

    @staticmethod
    def exinfo():
        return traceback.format_exc()


#
# def Colors(text, fcolor=None,bcolor=None,style=None):
#     '''
#     自定义字体样式及颜色
#     '''
#     # 字体颜色
#     fg={
#        'black': '\033[30m',     #字体黑
#        'red': '\033[31m',       #字体红
#        'green': '\033[32m',     #字体绿
#        'yellow': '\033[33m',    #字体黄
#        'blue': '\033[34m',      #字体蓝
#        'magenta': '\033[35m',   #字体紫
#        'cyan': '\033[36m',      #字体青
#        'white':'\033[37m',      #字体白
#         'end':'\033[0m'         #默认色
#     }
#     # 背景颜色
#     bg={
#        'black': '\033[40m',     #背景黑
#        'red': '\033[41m',       #背景红
#        'green': '\033[42m',     #背景绿
#        'yellow': '\033[43m',    #背景黄
#        'blue': '\033[44m',      #背景蓝
#        'magenta': '\033[45m',   #背景紫
#        'cyan': '\033[46m',      #背景青
#        'white':'\033[47m',      #背景白
#     }
#     # 内容样式
#     st={
#         'bold': '\033[1m',      #高亮
#         'url': '\033[4m',       #下划线
#         'blink': '\033[5m',     #闪烁
#         'seleted': '\033[7m',   #反显
#     }
#
#     if fcolor in fg:
#         text=fg[fcolor]+text+fg['end']
#     if bcolor in bg:
#         text = bg[bcolor] + text + fg['end']
#     if style in st:
#         text = st[style] + text + fg['end']
#     return text


if __name__ == "__main__":
    a = Pylog()
    Pylog.info("12345678")
