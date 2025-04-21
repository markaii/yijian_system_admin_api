import logging
from datetime import datetime
from common.wechat import wechat_wxa, wechatPay
from project import settings

from shop import constants as c
from shop import models

from boss import models as boss_models
from activity import models as activity_models
from activity import constants as activity_c

logger = logging.getLogger("send_subscribe_message")
red_packet_logger = logging.getLogger("send_red_packet")


def modify_shop_status(shop_id, shop_status, remark):
    """
    修改店铺状态,同时更新老板账号状态
    :param shop_ids:
    :param shop_status:
    :param remark:
    :return:
    """
    # 参数校验
    if not shop_id or not str(shop_status):
        return False, c.API_MESSAGE_PARAM_ERROR

    # 更新店铺状态
    try:
        shop = models.Shop.objects.get(id=shop_id)
    except models.Shop.DoesNotExist:
        return False, c.API_MESSAGE_PARAM_ERROR

    shop.status = shop_status
    shop.remark = remark
    shop.save()

    # 更新老板账号状态
    if shop_status == c.SHOP_STATUS_ENABLED:
        boss_models.Boss.objects.filter(shop_id=shop_id).update(status=c.STATUS_NORMAL)
    else:
        boss_models.Boss.objects.filter(shop_id=shop_id).update(status=c.STATUS_DISABLED)

    # 更新邀请入驻审核状态
    inviter_log = activity_models.ShopInviteLog.objects.filter(shop_id=shop_id).first()
    if inviter_log:
        if shop_status == c.SHOP_STATUS_ENABLED:
            inviter_log.status = activity_c.SHOP_INVITE_STATUS_PASSED
            # 审核通过，发送微信红包
            # _send_wechat_redpack(inviter_log)
        elif shop_status == c.SHOP_STATUS_APPROVE:
            inviter_log.status = activity_c.SHOP_INVITE_STATUS_REFUSE
        inviter_log.save()

    return True, shop


def batch_approve(shop_ids, shop_status, remark):
    """
    批量审核店铺
    :param shop_ids:
    :param shop_status:
    :param remark:
    :return:
    """
    if not shop_ids or not str(shop_status):
        return False, c.API_MESSAGE_PARAM_ERROR
    if not models.Shop.objects.filter(id__in=shop_ids).update(status=int(shop_status), remark=remark):  # 更新店铺状态
        return False, c.ERROR_SHOP_LOG_EXIST
    # 更新老板账号状态
    if int(shop_status) == c.SHOP_STATUS_ENABLED:
        boss_models.Boss.objects.filter(shop_id__in=shop_ids).update(status=c.STATUS_NORMAL)  # 如果审核通过，店铺老板账号更新状态
    else:
        boss_models.Boss.objects.filter(shop_id__in=shop_ids).update(status=c.STATUS_DISABLED)

    return True, c.API_MESSAGE_OK


def send_subscribe_message(shop):
    """
    发送审核结果模板消息
    """
    now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    approve_type = '店铺入驻申请'
    page = 'pages/examine/index?status=%s&shop_id=%s&shop_name=%s' % (shop.status, shop.id, shop.name)

    # 获取老板的openid
    boss = boss_models.Boss.objects.filter(shop_id=shop.id).first()

    # 审核结果
    if shop.status == c.SHOP_STATUS_ENABLED:
        data = {
            "thing8": {"value": approve_type},
            "phrase3": {"value": "通过"},
            "time4": {"value": now}
        }

        # 给用户发送通知
        try:
            wechat_wxa.send_subscribe_message(boss.openid, settings.WECHAT_MINIAPP_APPROVE_ENABLED_TEMPLATE, data,
                                              page)
        except Exception as e:
            logger.error(e)
    else:
        message = shop.remark

        data = {
            "thing1": {"value": approve_type},
            "date2": {"value": now},
            "phrase5": {"value": "失败"},
            "thing10": {"value": message}
        }

        # 给用户发送通知
        try:
            wechat_wxa.send_subscribe_message(boss.openid, settings.WECHAT_MINIAPP_APPROVE_DISABLED_TEMPLATE, data,
                                              page)
        except Exception as e:
            logger.error(e)


def _send_wechat_redpack(inviter_log):
    """
    发送微信红包
    :return:
    """
    try:
        res = wechatPay.redpack.send(inviter_log.inviter_openid, int(inviter_log.inviter_award_amount * 100), '逸剪',
                                     '邀请入驻活动',
                                     '好友入驻成功奖励现金红包%s元' % inviter_log.inviter_award_amount, '1')
    except Exception as e:
        logger.error(e)
        return False
    red_packet_logger.info(res)
    return True
