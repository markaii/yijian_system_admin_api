import time
import random
import logging

from project.celery import app as celery_app

from task import services
from task import constants as c
from task import models

logger = logging.getLogger('django')

@celery_app.task()
def collect_shop_info(task_id):
    """
    采集店铺信息
    先获取抓取页面的所有子链接，再循环抓取子链接数据
    :param task_id:
    :return:
    """
    task = models.ShopCollectTask.objects.get(id=task_id)

    # 初始化URL列表
    urls = []

    # 采集信息
    for number in range(c.start_page, c.end_page):
        time.sleep(random.randint(10, 20))
        try:
            if number == 1:
                url = task.initial_url
            else:
                url = '{}/p{}'.format(task.initial_url, str(number))

            # 发起请求，获取网页源码
            html = services.get_html_taxt(url, task.cookie)

            # 循环子链接, 抓取子链接数据
            for item in services.parser_sub_link(html, urls):
                html = services.get_html_taxt(item, task.cookie)
                # 数据存入
                try:
                    services.parser_data(html, task)
                except Exception as e:
                    time.sleep(2)
                    logger.info(e)
                    continue
                # 睡6,9秒
                time.sleep(random.randint(600, 700))
        except Exception as e:
            time.sleep(1)
            logger.info(e)
            continue

        # 清空子链接列表
        urls.clear()

    log = models.ShopCollectLog.objects.filter(task_id=task.id)

    # 修改任务状态
    if log.count() >= 50:
        task.status=c.SHOP_COLLECT_STATUS_ENABLED
    else:
        task.status = c.SHOP_COLLECT_STATUS_FAIL
    task.save()

    # 批量发送短信
    services.send_sms_batch(task.id)
