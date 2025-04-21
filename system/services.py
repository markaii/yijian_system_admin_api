import hashlib
import json
import time

import requests

from common.cos import cos_client
from project import settings

from uuid import uuid4
from sts.sts import Sts
from common.wechat import wechat_client, wechat_wxa
from system import constants as c


def create_key_name(file_name):
    """
    生成文件上传的key
    使用uuid
    :return:
    """
    if file_name:
        arr = file_name.split('.')
        if len(arr) == 2:
            ext = arr[1]
            timestamp = str(time.time())
            tmp_str = file_name + timestamp
            hash_str = hashlib.md5(tmp_str.encode('utf-8')).hexdigest()
            return '%s.%s' % (hash_str, ext)
        else:
            return uuid4().hex
    else:
        return uuid4().hex


def get_cos_sign(file_name):
    """
    获取cos文件上传的签名
    :return:
    """

    key = '%s/%s' % (settings.COS_STATIC_BASE_PATH, create_key_name(file_name))
    resp = cos_client.get_auth(
        Method='POST',
        Bucket=settings.QCLOUD_STORAGE_OPTION['Bucket'],
        Key=key
    )
    print(resp)
    return resp, key


def gen_temp_secret():
    """获取临时密钥"""
    config = {
        'url': 'https://sts.tencentcloudapi.com/',
        'domain': 'sts.tencentcloudapi.com',
        # 临时密钥有效时长，单位是秒
        'duration_seconds': 1800,
        'secret_id': settings.QCLOUD_STORAGE_OPTION['SecretId'],
        # 固定密钥
        'secret_key': settings.QCLOUD_STORAGE_OPTION['SecretKey'],

        # 换成你的 bucket
        'bucket': settings.QCLOUD_STORAGE_OPTION['Bucket'],
        # 换成 bucket 所在地区
        'region': settings.QCLOUD_STORAGE_OPTION['Region'],
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
        # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
        'allow_prefix': '*',
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': [
            # 简单上传
            'name/cos:PutObject',
            'name/cos:PostObject',
            # 分片上传
            'name/cos:InitiateMultipartUpload',
            'name/cos:ListMultipartUploads',
            'name/cos:ListParts',
            'name/cos:UploadPart',
            'name/cos:CompleteMultipartUpload'
        ],

    }
    try:
        sts = Sts(config)
        response = sts.get_credential()
        return response
    except Exception as e:
        print(e)


def create_mp_menu(menu):
    """
    设置菜单
    :return:
    """
    # menu = {
    #     "button": [
    #         {
    #             "name": "惠服务",
    #             "sub_button": [
    #                 {
    #                     "type": "miniprogram",
    #                     "name": "全民会加油",
    #                     "url": "https://shop90306984.m.youzan.com/v2/feature/r981VYTHFe",
    #                     "appid": "wxfa3384d2b7781120",
    #                     "pagepath": "pages/index/index"
    #                 },
    #             ]
    #         },
    #         {
    #             "name": "惠加油",
    #             "sub_button": [
    #                 {
    #                     "type": "miniprogram",
    #                     "name": "行业车",
    #                     "url": "https://shop90306984.m.youzan.com/v2/feature/r981VYTHFe",
    #                     "appid": "wxfa3384d2b7781120",
    #                     "pagepath": "pages/cert/index"
    #                 }
    #             ]
    #         },
    #         {
    #             "name": "惠生活",
    #             "sub_button": [
    #                 {
    #                     "type": "miniprogram",
    #                     "name": "在线办卡",
    #                     "url": "https://shop90306984.m.youzan.com/v2/feature/r981VYTHFe",
    #                     "appid": "wxfa3384d2b7781120",
    #                     "pagepath": "pages/card/index"
    #                 }
    #             ]
    #         }
    #     ]
    # }
    print(wechat_client.access_token)
    wechat_client.menu.create(menu)


def get_url_scheme(path, query):
    """
    获取小程序scheme码
    :param path:
    :param query:
    :return:
    """
    access_token = wechat_wxa.access_token
    url = c.WECHAT_BASE_URL + c.WECHAT_GEN_URL_SCHEME.format(access_token=access_token)
    exprie_time = int(time.time()) - 60 + (30 * 24 * 3600)
    data = {
        "jump_wxa":
            {
                "path": path,
                "query": query
            },
        "expire_time": int(exprie_time)
    }
    resp = requests.post(url=url, data=json.dumps(data))
    result = resp.json()
    err = result.get('errcode')
    if err != 0:
        return False, result['errmsg']
    return True, result['openlink']
