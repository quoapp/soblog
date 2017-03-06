import request
import json
import base64


def login(username, password):
    username = base64.b64encode(username.encode('utf-8')).decode('utf-8')
