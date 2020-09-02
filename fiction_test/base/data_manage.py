import os
import re

import yaml


def read_file(filename):  # 读取文件，请将文件放置在data目录下
    # noinspection PyBroadException
    try:
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + 'data' + os.sep + filename
        if re.match(r'[\S]+[.yaml]$', filename):
            with open(path, 'r') as file:
                result = yaml.load(file, Loader=yaml.FullLoader)
                return result
        else:
            with open(path, 'r') as file:
                result = file.read()
                return result
    except Exception:
        raise Exception('读取文件失败')