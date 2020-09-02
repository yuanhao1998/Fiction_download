import requests


def get_url(url, params=None, **kwargs):  # GET请求
    response = requests.get(url, params=None, **kwargs)
    return response


def post_url(url, data=None, json=None, **kwargs):  # POST请求
    response = requests.post(url, data, json, **kwargs)
    return response


def del_url(url, **kwargs):
    response = requests.delete(url, **kwargs)
    return response


def put(url, data=None, **kwargs):
    response = requests.put(url, data, **kwargs)
    return response
