from project.constants import *

# 采集任务状态
SHOP_COLLECT_STATUS_NOT = 0
SHOP_COLLECT_STATUS_ENABLED = 1
SHOP_COLLECT_STATUS_FAIL = 2
SHOP_COLLECT_STATUS_RUNING = 3
SHOP_COLLECT_STATUS_CHOICE = Choices(
    (SHOP_COLLECT_STATUS_NOT, '未采集'),
    (SHOP_COLLECT_STATUS_ENABLED, '已采集'),
    (SHOP_COLLECT_STATUS_FAIL, '采集中断'),
    (SHOP_COLLECT_STATUS_RUNING, '采集中')
)

# 短信发送状态
SMS_STATUS_NOT = 0
SMS_STATUS_ENABLED = 1
SMS_STATUS_CHOICES = Choices(
    (SMS_STATUS_NOT, '未发送'),
    (SMS_STATUS_ENABLED, '已发送')
)

# 店铺采集页数
start_page = 1
end_page = 51
