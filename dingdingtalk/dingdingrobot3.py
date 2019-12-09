#!/usr/bin/env python3

import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json

secret = 'SEC1872db19826828bfaabbed2dbce6982e9e10ed983645a8cb18ce996d912b63ca'
timestamp = round(time.time() * 1000)
secret_enc = bytes(secret, 'utf-8')
string_to_sign = '{}\n{}'.format(timestamp, secret)
string_to_sign_enc = bytes(string_to_sign, 'utf-8')
hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

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
    url = 'https://oapi.dingtalk.com/robot/send?access_token=2119679476e921a5025195258ecd064825ac5fb032e18d90a3ef20036dc02d10' + '&timestamp=' + str(timestamp) + '&sign=' + sign

    #print(url)
    print(send_msg(url))
