#!/usr/bin/env python2.7
# coding:utf-8

import time
import hmac
import hashlib
import base64
import urllib
import requests
import json

secret = 'your_secret'
timestamp = long(round(time.time() * 1000))
secret_enc = bytes(secret).encode('utf-8')
string_to_sign = '{}\n{}'.format(timestamp, secret)
string_to_sign_enc = bytes(string_to_sign).encode('utf-8')
hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = urllib.quote_plus(base64.b64encode(hmac_code))

print('timestamp', timestamp)
print('sign', sign)


def send_msg(url):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
        "msgtype": "text",
        "text": {
            "content": "测试消息",
        }
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.text


if __name__ == '__main__':
    url = 'https://oapi.dingtalk.com/robot/send?access_token=your_access_token' \
    + '&timestamp=' + str(timestamp) + '&sign=' + sign

    #print(url)
    print(send_msg(url))
