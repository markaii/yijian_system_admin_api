import logging
import hashlib
import os
import binascii
from base import constants as c, models

from uuid import uuid4
from datetime import datetime

logger = logging.getLogger('django')


def _generate_random_str(digital):
    """
    生成随机数
    :param digital: 数字位数
    :return:
    """
    return binascii.hexlify(os.urandom(digital)).decode()


def _generate_user_salt(user):
    """
    生成用户密码随机盐salt
    :param user:
    :return:
    """
    user.salt = _generate_random_str(10)
    user.save()
    return user.salt


def _is_register(account):
    """
    是否存在该注册的用户
    :param account:
    :return:
    """
    return models.User.objects.filter(account=account).exists()


def generate_user_token(user):
    """
    生成微信用户token
    :return: 新生成的token
    """
    user.token = _generate_random_str(10)
    user.save()
    return user.token


def check_user_password(user, old_password):
    """
    判断用户的密码是否正确
    :param user: User模型对象
    :param old_password: 密码
    :return:
    """
    return encrypt_password(user.salt, old_password) == user.password


def encrypt_password(salt, password):
    """
    使用sha1 和随机盐 加密明文密码
    :param password: 明文密码
    :param salt: 随机盐
    :return: 加密后的密码
    """
    # logger.debug('encrypt:' + salt)
    # logger.debug('encrypt:' + password)
    # logger.debug('encrypt:' + salt + password)
    # logger.debug('encrypt:' + hashlib.md5(salt + password).hexdigest())

    return hashlib.md5((salt + password).encode('utf-8')).hexdigest()


def logout(user):
    """
    退出登录
    删除相关用户的token
    :param user: 当前用户
    :return:
    """
    user.token = ''
    user.save()
    return True, c.API_MESSAGE_OK


def login(account, password):
    """
    登录，使用账号和密码登录
    :param account:
    :param password:
    :return:
    """
    logger.debug("fun login:" + account)
    logger.debug("fun login:" + password)
    if not _is_register(account=account):
        return False, c.ERROR_PHONE_UNREGISTERED
    user = models.User.objects.get(account=account)
    logger.debug("fun login:" + encrypt_password(user.salt, password))
    logger.debug("fun login:" + user.password)
    if encrypt_password(user.salt, password) != user.password:
        return False, c.ERROR_ACCOUNT_PASSWORD_ERROR
    # token操作
    generate_user_token(user)
    # 登录成功
    return True, user


def login_log(account, meta, resp, code):
    """
    登录日志
    """
    user = models.User.objects.get(account=account)
    ip_address = meta.get("REMOTE_ADDR")
    host = meta.get("REMOTE_HOST", 'unknown')
    browser = meta.get('HTTP_USER_AGENT', 'unknown')

    log = models.Log.objects.create(type=c.LOG_TYPE_LOGIN, module_name=c.LOG_MODULE_NMAE, operate_user_id=user.id,
                                    operate_user=user.realname, operate_time=datetime.now(),
                                    ip_address=ip_address, host=host, browser=browser, operate_type=c.LOG_TYPE_CHOICE[c.LOG_TYPE_LOGIN])
    if not resp:
        log.result_type = c.LOG_RESULT_FAILED
        log.result_desc = c.ERROR_CHOICE[code]
        log.save()
    else:
        log.result_type = c.LOG_RESULT_SUCCESS
        log.save()


def modify_password(user, new_password):
    """
    修改密码
    :param user: 用户
    :param new_password: 新密码
    :return:
    """
    user.password = encrypt_password(user.salt, new_password)
    user.save()
    return True, user


def reset_password(user_id, new_password):
    """
    修改密码
    :param user_id: 用户_id
    :param new_password: 新密码
    :return:
    """
    user = models.User.objects.get(id=user_id)
    print(user.password)
    print("*"*100)
    user.password = encrypt_password(user.salt, new_password)
    user.save()
    print(user.password)
    return True, user


def role_authorize(role_id, data):
    """
    角色功能授权
    """
    # 首先删除原有的授权
    models.Authorize.objects.filter(object_id=role_id).delete()
    try:
        for item in data["module_list"]:
            print(item)

            module_obj = models.Authorize(object_type=c.AUTHORIZE_OBJECT_TYPE_ROLE, object_id=role_id,
                                          item_type=c.AUTHORIZE_ITEM_TYPE_MODULE, item_id=item
                                          )
            module_obj.save()

        for item in data["button_list"]:
            button_obj = models.Authorize(object_type=c.AUTHORIZE_OBJECT_TYPE_ROLE, object_id=role_id,
                                          item_type=c.AUTHORIZE_ITEM_TYPE_BUTTON, item_id=item
                                          )
            button_obj.save()

        for item in data["column_list"]:
            column_obj = models.Authorize(object_type=c.AUTHORIZE_OBJECT_TYPE_ROLE, object_id=role_id,
                                          item_type=c.AUTHORIZE_ITEM_TYPE_VIEW, item_id=item
                                          )
            column_obj.save()

        for item in data["form_list"]:
            form_obj = models.Authorize(object_type=c.AUTHORIZE_OBJECT_TYPE_ROLE, object_id=role_id,
                                        item_type=c.AUTHORIZE_ITEM_TYPE_FORM, item_id=item
                                        )
            form_obj.save()
    except Exception as e:
        print(e)
        return False
    return True


def user_authorize(user_id, data):
    """
    用户功能授权
    """
    # 首先删除原有的授权
    models.Authorize.objects.filter(object_id=user_id).delete()
    try:
        for item in data["module_list"]:
            module_obj = models.Authorize(object_type=c.AUTHORIZE_OBJECT_TYPE_USER, object_id=user_id,
                                          item_type=c.AUTHORIZE_ITEM_TYPE_MODULE, item_id=item
                                          )
            module_obj.save()

        for item in data["button_list"]:
            button_obj = models.Authorize(object_type=c.AUTHORIZE_OBJECT_TYPE_USER, object_id=user_id,
                                          item_type=c.AUTHORIZE_ITEM_TYPE_BUTTON, item_id=item
                                          )
            button_obj.save()

        for item in data["column_list"]:
            column_obj = models.Authorize(object_type=c.AUTHORIZE_OBJECT_TYPE_USER, object_id=user_id,
                                          item_type=c.AUTHORIZE_ITEM_TYPE_VIEW, item_id=item
                                          )
            column_obj.save()

        for item in data["form_list"]:
            form_obj = models.Authorize(object_type=c.AUTHORIZE_OBJECT_TYPE_USER, object_id=user_id,
                                        item_type=c.AUTHORIZE_ITEM_TYPE_FORM, item_id=item
                                        )
            form_obj.save()
    except Exception as e:
        print("*"*50)
        print(e)
        return False
    return True


def remove_sub_modules(module):
    """
    删除模块关联的子模块
    :param module:
    :return:
    """
    models.ModuleButton.objects.filter(module_id=module.id).delete()
    models.ModuleColumn.objects.filter(module_id=module.id).delete()
    models.ModuleForm.objects.filter(module_id=module.id).delete()


def create_sub_modules(module, button_list, column_list, form_list):
    """
    创建模块关联的子模块
    :param module:
    :param button_list:
    :param column_list:
    :param form_list:
    :return:
    """
    for item in button_list:
        sort = item.get('sort', 0)
        models.ModuleButton.objects.create(module_id=module.id, name=item['name'],
                                           code=item['code'], sort=sort)
    for item in column_list:
        sort = item.get('sort', 0)
        models.ModuleColumn.objects.create(module_id=module.id, name=item['name'],
                                           code=item['code'], sort=sort)
    for item in form_list:
        sort = item.get('sort', 0)
        models.ModuleForm.objects.create(module_id=module.id, name=item['name'],
                                         code=item['code'], sort=sort)


def create_key_name():
    """
    生成文件阿里云上传的key
    使用uuid
    :return:
    """
    return uuid4().hex


def update_company_parent_id():
    """
    更新公司parent_id
    :return:
    """
    qs = models.Company.objects.filter(parent_id='')
    for item in qs:
        if item.parent_ou_code == '':
            continue
        print(item)
        try:
            parent = models.Company.objects.get(ou_code=item.parent_ou_code)
            item.parent_id = parent.id
            item.save()
        except Exception as e:
            continue
