from django.core.cache import caches
from project import settings
from wechatpy.client import WeChatClient, WeChatComponentClient
from wechatpy import WeChatComponent, WeChatPay
from wechatpy.crypto import WeChatCrypto

# 消费者小程序
wechat_wxa = WeChatClient(settings.WECHAT_MINIAPP_APPID, settings.WECHAT_MINIAPP_APPSECRET).wxa

# # 公众号端
wechat_client = WeChatClient(settings.WECHAT_MP_APPID, settings.WECHAT_MP_APP_SECRET)

# 全局的微信支付
wechatPay = WeChatPay(settings.WECHAT_MP_APPID, settings.WECHAT_PAY_MCH_KEY,
                      settings.WECHAT_PAY_MCH_ID,
                      mch_cert=settings.WECHAT_PAY_MCH_CERT, mch_key=settings.WECHAT_PAY_MCH_CERT_KEY)
