import re

import requests


def get_page(url, headers=None, encoding='utf-8'):  # get������ȡҳ��
    if not re.match(r'^http:', url):
        url = 'http://' + url
    return requests.get(url=url, headers=headers).content.decode(encoding=encoding)


def post_page(url, headers=None, data=None, encoding='utf-8'):  # post������ȡҳ��
    if not re.match(r'^http:', url):
        url = 'http://' + url
    return requests.post(url=url, headers=headers, data=data).content.decode(encoding=encoding)
