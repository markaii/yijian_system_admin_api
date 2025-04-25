from common.serializers import BaseModelSerializer
from rest_framework import serializers
from member import models


class MemberCardSimpleSerializers(BaseModelSerializer):
    """
    商家会员卡简单序列化器
    """

    class Meta:
        model = models.MemberCard
        fields = '__all__'


class MemberCardSerializers(BaseModelSerializer):
    """
    商家会员卡序列化器
    """
    discount_list = serializers.SerializerMethodField()
    coupon_list = serializers.SerializerMethodField()
    charge_rule_list = serializers.SerializerMethodField()

    def get_discount_list(self, obj):
        """折扣列表"""
        qs = models.MemberCardDiscount.objects.filter(card_id=obj.id)
        serializer = MemberCardDiscountSerializers(qs, many=True)
        return serializer.data

    def get_coupon_list(self, obj):
        """优惠券列表"""
        qs = models.MemberCardCoupon.objects.filter(card_id=obj.id)
        serializer = MemberCardCouponSerializers(qs, many=True)
        return serializer.data

    def get_charge_rule_list(self, obj):
        """充值折扣列表"""
        qs = models.MemberCardChargeRule.objects.filter(card_id=obj.id)
        serializer = MemberCardChargeRuleSerializers(qs, many=True)
        return serializer.data

    class Meta:
        model = models.MemberCard
        fields = '__all__'


class MemberCardDiscountSerializers(BaseModelSerializer):
    """
    商家会员卡折扣序列化器
    """

    class Meta:
        model = models.MemberCardDiscount
        fields = '__all__'


class MemberCardCouponSerializers(BaseModelSerializer):
    """
    商家会员卡关联优惠券序列化器
    """

    class Meta:
        model = models.MemberCardCoupon
        fields = '__all__'


class MemberCardChargeRuleSerializers(BaseModelSerializer):
    """
    商家会员卡关联充值充值规则序列化器
    """

    class Meta:
        model = models.MemberCardChargeRule
        fields = '__all__'


class MemberCardInstanceSerializers(BaseModelSerializer):
    """
    用户会员卡序列化器
    """

    class Meta:
        model = models.MemberCardInstance
        fields = '__all__'


class MemberCardInstanceDiscountSerializers(BaseModelSerializer):
    """
    用户会员卡关联折扣序列化器
    """

    class Meta:
        model = models.MemberCardInstanceDiscount
        fields = '__all__'


class MemberCardInstanceChargeRuleSerializers(BaseModelSerializer):
    """
    用户会员卡关联充值优惠规则序列化器
    """

    class Meta:
        model = models.MemberCardInstanceChargeRule
        fields = '__all__'


class MemberCardChargeLogSerializers(BaseModelSerializer):
    """
    用户会员卡充值记录序列化器
    """

    class Meta:
        model = models.MemberCardChargeLog
        fields = '__all__'


class MemberCardConsumeLogSerializers(BaseModelSerializer):
    """
    用户会员卡消费记录序列化器
    """

    class Meta:
        model = models.MemberCardConsumeLog
        fields = '__all__'


class MemberChargeOrderSerializers(BaseModelSerializer):
    """
    充值订单序列化器
    """

    class Meta:
        model = models.MemberChargeOrder
        fields = '__all__'
