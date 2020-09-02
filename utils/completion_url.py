import re


def Completion_URL(url):  # ²¹È«URLÁ´½Ó
    if not re.match(r'^http:', url):
        url = 'http://' + url
    return url