# 数据库路由
# 订单库是独立的
# 库存库是独立的
XSM_MODELS = [
    'ZxCo',
    'ZxCoLine',
    'ZxItem',
    'SaleReportV3Chengdu',
    'ZxBuy',
    'ZxDataGoods',
    'ZxDataShop',
]

POS_V3_MODELS = [
    'V3Shops',  # 店铺
    'V3Goods',  # 商品
    'V3Orders',  # 订单
    'V3OrderGoods',  # 订单详情
    'V3SplitRule',  # 转换规则
    'V3GoodsStock',

]


# 新增路由
class ShopDbRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.object_name in POS_V3_MODELS:
            return 'posv3'
        if model._meta.object_name in XSM_MODELS:
            return 'xsm'
        return 'default'

    def db_for_write(self, model, **hints):
        "Point all operations on chinook models to 'xsm'"
        if model._meta.object_name in POS_V3_MODELS:
            return 'posv3'
        if model._meta.object_name in XSM_MODELS:
            return 'xsm'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a both models in xsm app"
        if obj1._meta.object_name in XSM_MODELS and obj2._meta.object_name in XSM_MODELS:
            return True
        # Allow if neither is chinook app
        elif 'xsm' not in [obj1._meta.object_name, obj2._meta.object_name]:
            return True
        return False

    def allow_syncdb(self, db, model):
        if db == 'posv3' or model._meta.object_name == "posv3":
            return False  # we're not using syncdb on our legacy database
        if db == 'xsm' or model._meta.object_name == "xsm":
            return False  # we're not using syncdb on our legacy database
        else:  # but all other models/databases are fine
            return True
