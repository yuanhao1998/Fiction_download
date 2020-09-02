import json


def load(response):
    return json.loads(response.content.decode())