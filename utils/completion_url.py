import re


def Completion_URL(url):  # ��ȫURL����
    if not re.match(r'^http:', url):
        url = 'http://' + url
    return url