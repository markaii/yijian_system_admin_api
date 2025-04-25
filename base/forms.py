from django import forms


class LoginForm(forms.Form):
    """登录的form"""
    account = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class PasswordForm(forms.Form):
    """检查密码的form"""
    password = forms.CharField(required=True, min_length=6)


class ModifyPasswordForm(forms.Form):
    """修改密码的form"""
    new_password = forms.CharField(required=True, min_length=6)


class ResetPasswordForm(forms.Form):
    """重置密码的form"""
    # mobile = forms.CharField(required=True)
    # code = forms.CharField(required=True)  # 短信验证码
    user_id = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class LogDeleteForm(forms.Form):
    type = forms.IntegerField(required=True)
    start_time = forms.DateField(required=True)
    end_time = forms.DateField(required=True)


class LogDateFilter(forms.Form):
    start_time = forms.CharField(required=True)
    end_time = forms.CharField(required=True)
    type = forms.IntegerField(required=True)


# class PostAddMember(forms.Form):
#     """职位添加成员的form"""
#     post_id = forms.CharField(required=True)
#     person_list = forms.CharField(required=True)


class UserPost(forms.Form):
    """职位关联用户的form"""
    post_id = forms.CharField(required=True)


class RoleAddMember(forms.Form):
    """角色添加成员的form"""
    role_id = forms.CharField(required=True)
    user_id = forms.CharField(required=True)


class UserRole(forms.Form):
    """角色关联用户的form"""
    role_id = forms.CharField(required=True)


class AuthorizeForm(forms.Form):
    """角色功能授权的form"""
    role_id = forms.CharField(required=True)       # 授权对象主键
    module_list = forms.CharField(required=True)
    button_list = forms.CharField(required=True)
    column_list = forms.CharField(required=True)
    form_list = forms.CharField(required=True)






