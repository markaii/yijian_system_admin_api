from common.serializers import BaseModelSerializer
from coupon import models


class CouponSerializers(BaseModelSerializer):
    """
    优惠券列化器
    """
    class Meta:
        model = models.Coupon
        fields = '__all__'


class CouponVoucherSerializers(BaseModelSerializer):
    """
    优惠券记录列化器
    """
    class Meta:
        model = models.CouponVoucher
        fields = '__all__'
