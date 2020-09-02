import re

import requests

from utils.completion_url import Completion_URL


def get_page(url, headers=None, encoding='utf-8'):  # get������ȡҳ��
    return requests.get(url=Completion_URL(url), headers=headers).content.decode(encoding=encoding)


def post_page(url, headers=None, data=None, encoding='utf-8'):  # post������ȡҳ��
    return requests.post(url=Completion_URL(url), headers=headers, data=data).content.decode(encoding=encoding)