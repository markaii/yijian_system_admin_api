from common.serializers import BaseModelSerializer
from rest_framework.serializers import SerializerMethodField

from activity import models


class BannerSerializers(BaseModelSerializer):
    """
    小程序广告配置序列化器
    """

    class Meta:
        model = models.Banner
        fields = '__all__'


class ShopInviteActivitySerializers(BaseModelSerializer):
    """
    店铺邀请入驻活动列化器
    """

    class Meta:
        model = models.ShopInviteActivity
        fields = '__all__'


class ShopInviteLogSerializers(BaseModelSerializer):
    """
    店铺入驻邀请记录序列化器
    """

    class Meta:
        model = models.ShopInviteLog
        fields = '__all__'


class ShopPosterApplySerializers(BaseModelSerializer):
    """
    店铺物料申请序列化器
    """

    class Meta:
        model = models.ShopPosterApply
        fields = '__all__'


class ShopPosterApplyLogSerializers(BaseModelSerializer):
    """
    店铺物料申请记录序列化器
    """

    class Meta:
        model = models.ShopPosterApplyLog
        fields = '__all__'


class ShopCouponActivitySerializers(BaseModelSerializer):
    """
    店铺优惠券活动序列化器
    """

    class Meta:
        model = models.ShopCouponActivity
        fields = '__all__'


class ShopPinSerializers(BaseModelSerializer):
    """
    拼团序列化器
    """

    class Meta:
        model = models.ShopPin
        fields = '__all__'


class ShopPinLogSerializers(BaseModelSerializer):
    """
    拼团记录序列化器
    """
    pin_status = SerializerMethodField()

    def get_pin_status(self, obj):
        """拼团状态"""
        group = models.ShopPin.objects.get(id=obj.pin_id)
        return group.status

    class Meta:
        model = models.ShopPinLog
        fields = '__all__'


class ShopPinAwardRulesSerializers(BaseModelSerializer):
    """
    拼团奖励规则序列化器
    """

    class Meta:
        model = models.ShopPinAwardRules
        fields = '__all__'


class ShopPinAwardLogSerializers(BaseModelSerializer):
    """
    拼团领奖记录序列化器
    """

    class Meta:
        model = models.ShopPinAwardLog
        fields = '__all__'
