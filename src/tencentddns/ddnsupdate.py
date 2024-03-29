import requests
import json
import os
import sys
import datetime
import time

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.dnspod.v20210323 import dnspod_client, models

cur_path = os.path.abspath(os.path.dirname(__file__))
print(cur_path)
sys.path.insert(0, cur_path+"/../../")

from src.util.Ipv6Util import getIpv6

# 输出日志
def log(info):
    path = cur_path + "/log.txt"
    if os.path.exists(path):
        datetime_object = datetime.datetime.now()
        datetime_object = str(datetime_object)
        datetime_object = datetime_object[0:datetime_object.index(".", 18)]
        logInfo = "{} {}\n".format(datetime_object, info)
        print(logInfo)
        with open(path, "ab") as f:
            f.write(logInfo.encode("utf-8"))


# 获取公共请求对象
def getReq():
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
        # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
        cred = credential.Credential("appKey", "appSecury")
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "dnspod.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = dnspod_client.DnspodClient(cred, "", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        # req = models.DescribeRecordRequest()
        reqJson = [models, client];
        return reqJson
    except TencentCloudSDKException as err:
        log(err)

# 获取全部信息
def getAllRecord(name):
    try:
        reqJson = getReq();
        params = {
            "Domain": name
        }
        req = reqJson[0].DescribeRecordListRequest()
        req.from_json_string(json.dumps(params))
        client = reqJson[1]

        # 返回的resp是一个DescribeRecordListResponse的实例，与请求对象对应
        resp = client.DescribeRecordList(req)
        # 输出json格式的字符串回包
        return resp.RecordList;

    except TencentCloudSDKException as err:
        log(err)

# 根据子域名获取信息
def getRecordInfo(domain, name):
    recordList = getAllRecord(domain)
    record = None;
    for obj in recordList:
        if (name == obj.Name):
            record = obj
            pass
        pass
    return record


# 根据记录id获取子域名详情
def getRecordDetail(name, recordId):
    try:
        reqJson = getReq()
        params = {
            "Domain": name,
            "RecordId": recordId
        }
        req = reqJson[0].DescribeRecordRequest()
        req.from_json_string(json.dumps(params))
        client = reqJson[1]

        # 返回的resp是一个DescribeRecordResponse的实例，与请求对象对应
        resp = client.DescribeRecord(req)
        # 输出json格式的字符串回包
        return resp.RecordInfo

    except TencentCloudSDKException as err:
        log(err)

# 更新ip地址
def updateDdns(domain, oldRecord, newIpv6Add):
    try:
        params = {
            "Domain": domain,
            "SubDomain": oldRecord.Name,
            "RecordType": oldRecord.Type,
            "RecordLine": oldRecord.Line,
            "RecordLineId": oldRecord.LineId,
            "Value": newIpv6Add,
            "RecordId": oldRecord.RecordId,
            "Weight": oldRecord.Weight
        }
        reqJson = getReq()
        req = reqJson[0].ModifyRecordRequest()
        req.from_json_string(json.dumps(params))
        client = reqJson[1]
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个ModifyRecordResponse的实例，与请求对象对应
        resp = client.ModifyRecord(req)
        # 输出json格式的字符串回包
        if resp.RequestId:
            log("更新成功")
        else:
            log(resp.to_json_string())

    except TencentCloudSDKException as err:
        log(err)

# 判断地址，进行更新
def checkValue(ipv6):
    sub = "test"
    domain = "test"
    record = getRecordInfo(domain, sub)
    if not record.Value == ipv6:
        log("最新地址：%s，历史地址：%s"%(ipv6, record.Value))
        updateDdns(domain, record, ipv6)

        # 更新cloudflare
        updateCloudflare(ipv6)
        # re = getRecordDetail(domain, record.RecordId);
        # print(re)
    else:
        log("地址相同，不用更新：%s"%(ipv6))

# 更新cloudflared地址
def updateCloudflare(ipv6):
    url = "https://api.cloudflare.com/client/v4/zones/xxxxx/dns_records/xxxxxx"

    payload = {
        "content": ipv6,
        "name": "xxxxxxxx",
        "proxied": True,
        "type": "AAAA",
        #"comment": "",
        #"tags": ["owner:dns-team"],
        "ttl": 60
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer xxxxxxxxxxxx"
    }

    response = requests.request("PUT", url, json=payload, headers=headers)
    rel = json.loads(response.text);
    if (rel["success"]):
        log("xxx更新成功")
    else:
        log("xxxx更新失败：%s"%(rel))

    # 查询列表
    # url = "https://api.cloudflare.com/client/v4/zones/xxxxx/dns_records"

    # headers = {
    #     "Content-Type": "application/json",
    #     "Authorization": "Bearer xxxxxx"
    # }

    # response = requests.request("GET", url, headers=headers)

    # print(response.text)

def startUpdate(count):
    ipv6 = getIpv6()
    if (len(ipv6) > 0):
        newAdd = ipv6[0]
        if (len(ipv6) > 1):
            newAdd = ipv6[1]
            pass
        checkValue(newAdd)
        pass
    else:
        count += 1
        log("Ipv6地址为空，第%d次"%(count))
        if count < 3:
            time.sleep(20)
            startUpdate(count)
        else:
            log("更新失败")


if __name__ == "__main__":
    log("开始更新地址")
    startUpdate(0)
    while True:
        log("保持运行")
        time.sleep(10800);