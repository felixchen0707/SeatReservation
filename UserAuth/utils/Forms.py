from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from Reservation import models
from UserAuth.utils.bootstrapForm import BootStrapForm


class RegisterForm(BootStrapForm, forms.ModelForm):
    password = forms.CharField(
        label="密码",
        max_length=64,
        widget=forms.PasswordInput(attrs={'placeholder': "请输入密码"}, render_value=True)
    )
    mobile_phone = forms.CharField(
        label="手机号",
        max_length=32,
        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误')]
    )
    check_password = forms.CharField(
        label="确认密码",
        max_length=64,
        widget=forms.PasswordInput(attrs={'placeholder': '确认密码'}, render_value=True)
    )
    verification_code = forms.CharField(
        label="图形验证码",
        max_length=10
    )

    class Meta:
        model = models.UserInfo
        exclude = ['identity', 'breaking']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_username(self):
        if models.UserInfo.objects.filter(username=self.cleaned_data["username"]).exists():
            raise ValidationError("用户名已存在")
        return self.cleaned_data['username']

    def clean_check_password(self):
        if not self.cleaned_data['password'] == self.cleaned_data['check_password']:
            raise ValidationError("两次密码不一致")
        return self.cleaned_data['check_password']

    def clean_verification_code(self):
        code_in_session = self.request.session['verification_code']
        if not code_in_session:
            raise ValidationError("验证码已过期")
        if not self.cleaned_data['verification_code'] == code_in_session:
            raise ValidationError("验证码错误")
        return self.cleaned_data['verification_code']


class LoginForm(BootStrapForm, forms.ModelForm):
    password = forms.CharField(
        label="密码",
        max_length=64,
        widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'}, render_value=True)
    )
    verification_code = forms.CharField(
        label="图形验证码",
        max_length=32
    )

    class Meta:
        model = models.UserInfo
        fields = ['username']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_password(self):
        row_obj = models.UserInfo.objects.filter(username=self.cleaned_data.get('username')).first()
        if row_obj and row_obj.password == self.cleaned_data['password']:
            return self.cleaned_data['password']
        else:
            raise ValidationError("用户名或密码错误")

    def clean_verification_code(self):
        code_in_session = self.request.session['verification_code']
        if not code_in_session:
            raise ValidationError("验证码已过期")
        if not self.cleaned_data['verification_code'] == code_in_session:
            raise ValidationError("验证码错误")
        return self.cleaned_data['verification_code']
