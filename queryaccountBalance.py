#!/usr/bin/env python3
# coding:utf-8
# 查询阿里云账号余额
# python3


import hashlib
import hmac
import base64
import urllib
import time
import uuid
import requests


def get_iso8601_time():
    """返回iso8601格式的时间"""
    format_iso8601 = "%Y-%m-%dT%H:%M:%SZ"
    return time.strftime(format_iso8601, time.gmtime())


def get_uuid():
    """返回uuid"""
    return str(uuid.uuid4())


def get_parameters(user_param, Action, AccessKeyId, Version):
    """
    拼接参数字典
    user_param: {"RegionId":"cn-beijing", "LoadBalancerName":"test-node1", "AddressType":"intranet", "VSwitchId":"vsw-2zevjlczuvp2mkhhch12x"}
    Action操作例如:CreateLoadBalancer
    AccessKeyId：access key ID
    Version: 接口的版本
    """
    parameters = {}
    parameters['HTTPMethod'] = 'GET'
    parameters['AccessKeyId'] = AccessKeyId
    parameters['Format'] = 'json'
    parameters['Version'] = Version
    parameters['SignatureMethod'] = 'HMAC-SHA1'
    parameters['Timestamp'] = get_iso8601_time()
    parameters['SignatureVersion'] = '1.0'
    parameters['SignatureNonce'] = get_uuid()
    parameters['Action'] = Action
    for (k, v) in sorted(user_param.items()):
        parameters[k] = v
    return parameters



def get_param(parameters):
    """把公共参数拼接成字符串"""
    param_str = ''
    for (k, v) in sorted(parameters.items()):
        param_str += "&" + urllib.request.quote(k, safe='') + "=" + urllib.request.quote(v, safe='')
    param_str = param_str[1:]
    return param_str


def get_StringToSign(parameters, param_str):
    """拼接生成签名的字符串"""
    string_to_sign = parameters['HTTPMethod'] + "&%2F&" + urllib.request.quote(param_str, safe='')
    return string_to_sign



def get_signature(StringToSign, AccessKeySecret):
    """构建签名"""
    h = hmac.new(AccessKeySecret.encode(), StringToSign.encode(), hashlib.sha1)
    signature = base64.b64encode(h.digest()).strip()
    return signature


def build_request(server_url, param_str, signature, AccessKeySecret):
    """拼接url并进行请求"""
    Signature = "Signature=" + urllib.request.quote(signature)
    param = param_str + "&" + Signature
    request_url = server_url + param
    s = requests.get(request_url)
    return s.content


def get_regions(server_url, Action, user_param, AccessKeySecret, AccessKeyId, Version):
    """对请求进行模块
    server_url： slb.aliyun.com
    Action = 'DescribeRegions'
    AccessKeySecret, AccessKeyId:也就是ak
    user_param = {'LoadBalancerId': 'lb-2zekxu2elibyexxoo9hlw'}
    Version:例如slb的版本是2014-05-15,每个服务都不相同
    """
    server_url = 'https://' + server_url + '/?'
    AccessKeySecret = AccessKeySecret
    AccessKeyId = AccessKeyId
    parameters = get_parameters(user_param, Action, AccessKeyId, Version)
    param_str = get_param(parameters)
    StringToSign = get_StringToSign(parameters, param_str)
    signature = get_signature(StringToSign, AccessKeySecret + '&')
    data = build_request(server_url, param_str, signature, AccessKeySecret)
    return data



if __name__ == "__main__":
    server_url = 'business.aliyuncs.com'
    AccessKeyId = 'your_ak'
    AccessKeySecret = 'your_aks'
    Version = '2017-12-14'

    Action = 'QueryAccountBalance'
    user_param = {}
    response = get_regions(server_url, Action, user_param, AccessKeySecret, AccessKeyId, Version)
    print(response)
