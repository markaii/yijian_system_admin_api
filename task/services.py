import requests
import re
import hashlib
import json

from bs4 import BeautifulSoup
from lxml import etree

from project import settings
from task import models
from task import constants as c


def get_html_taxt(url, cookie):
    """
    获取网页源码
    """
    try:
        header = {
            "cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"
        }
        result = requests.get(url, headers=header, timeout=30)
        result.raise_for_status()
        result.encoding = 'utf-8'
        return result.text
    except Exception as e:
        return None


def parser_sub_link(html, urls):
    """
    获取页面子链接
    """
    soup = BeautifulSoup(html, "html.parser")
    try:
        billing = soup.select('div[class="pic"] a')

        for i in billing:
            url = i['href']
            urls.append(url)
    except Exception as e:
        pass
    return urls


def get_timestamp():
    """
    获取时间戳
    """
    try:
        res = requests.get('https://api.mysubmail.com/service/timestamp').json()
        timestamp = str(res['timestamp'])
        return timestamp
    except:
        return None


def md5_encrypt(param):
    """
    md5加密
    """
    signStr = ''
    for key in sorted(param):
        signStr += key + '=' + param[key] + '&'
    signStr = signStr[:-1]
    signStr = settings.SUB_MAIL_APP_ID + settings.SUB_MAIL_APP_KEY + signStr + settings.SUB_MAIL_APP_ID + settings.SUB_MAIL_APP_KEY

    md5 = hashlib.md5()
    string = signStr.encode(encoding='utf-8')
    md5.update(string)
    return md5.hexdigest()


def parser_data(html, task):
    """
    数据清洗
    """
    soup = BeautifulSoup(html, "lxml")
    html = etree.HTML(html)

    # 数据清洗
    shop_name = html.xpath("//h1[@class='shop-name']")[0].text.strip(),  # 店铺名
    district = soup.select('span[itemprop="locality region"]')[0].text.strip(),  # 区
    address = soup.select('span[itemprop="street-address"]')[0].text.strip(),  # 地址
    phone = soup.select('p[class="expand-info tel"]')[0].text.strip()  # 手机号

    # 去除括号
    shop_name = shop_name[0].replace('(', '').replace(')', '') if shop_name else ""
    district = district[0].replace('(', '').replace(')', '') if district else ""
    address = address[0].replace('(', '').replace(')', '') if address else ""

    # 正则匹配手机号
    filters = re.search(r'1[3-9]\d{9}', phone)
    if filters:
        phone = filters.group() if filters else None

        # 判断是否存在相同记录
        if not models.ShopCollectLog.objects.filter(phone=phone).exists():
            # 创建采集记录
            models.ShopCollectLog.objects.create(name=shop_name, phone=phone, task_id=task.id,
                                                 task_name=task.name, city=task.city,
                                                 city_code=task.city_code, district=district,
                                                 district_code=task.district_code, address=address)


def send_sms_batch(task_id):
    """
    批量发送短信
    :return:
    """
    phone_list = models.ShopCollectLog.objects.filter(task_id=task_id, sms_status=c.SMS_STATUS_NOT).values_list('phone',
                                                                                                                flat=True)
    # 将列表分割成几份
    split_list = [phone_list[i:i + 100] for i in range(0, len(phone_list), 100)]

    # 循环分割后的列表，批量发送短信
    for item in split_list:

        # 主体信息
        multi = []
        for phone in item:
            multi.append({'to': phone})

        # 参数
        param = {
            'appid': settings.SUB_MAIL_APP_ID,
            'sign_version': settings.SUB_MAIL_SIGN_VERSION,
            'sign_type': settings.SUB_MAIL_SIGN_TYPE,
            'project': settings.SUB_MAIL_TEMPLATE_ID,
            'timestamp': get_timestamp()
        }
        param["signature"] = md5_encrypt(param)
        param["multi"] = json.dumps(multi)

        # 发送请求
        try:
            result = requests.post(settings.SUB_MAIL_URL, data=json.dumps(param),
                                   headers={"Content-type": "application/json"})
            # 响应处理
            for item in result.json():
                if item['status'] == 'success':
                    models.ShopCollectLog.objects.filter(phone=item['to']).update(sms_status=c.SMS_STATUS_ENABLED)
        except Exception as e:
            continue
