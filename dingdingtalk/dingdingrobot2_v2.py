#!/usr/bin/env python2.7
# coding:utf-8

import time
import hmac
import hashlib
import base64
import urllib
import requests
import json
import sys

def get_timestamp():
    timestamp = long(round(time.time() * 1000))
    return timestamp

def get_StringToSign(secret):
    secret = secret
    timestamp = get_timestamp()
    secret_enc = bytes(secret).encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = bytes(string_to_sign).encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.quote_plus(base64.b64encode(hmac_code))
    return sign


def send_msg(url):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
        "msgtype": "text",
        "text": {
            "content": content,
        }
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.text


if __name__ == '__main__':

    # reference https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
    secret = your_secret
    webhook = your_webook

    timestamp = get_timestamp()
    sign = get_StringToSign(secret)
    request_url = webhook  + '&timestamp=' + str(timestamp) + '&sign=' + sign

    content = sys.argv[1]
    send_msg(request_url)
