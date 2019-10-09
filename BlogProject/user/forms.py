from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='用户名或邮箱',widget=forms.TextInput(
                                attrs={'class':'form-control'}))
    password = forms.CharField(label='密码',widget=forms.PasswordInput(
                                attrs={'class':'form-control'}))

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data['user'] =user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=30,
                               min_length=3,
                               widget=forms.TextInput(
                                attrs={'class':'form-control'}))
    email = forms.EmailField(label='邮箱',
                               widget=forms.EmailInput(
                                attrs={'class':'form-control'}))
    verification_code = forms.CharField(label='验证码', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label='密码',min_length=6, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password_again = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean(self):
        code = self.request.session.get('register_email_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code

class ChangeNickForm(forms.Form):
    new_nickname =forms.CharField(label='新的昵称',max_length=30,widget=forms.TextInput(
                                attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNickForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] =self.user
        else:
            raise forms.ValidationError('用户未登录')
        return self.cleaned_data

    def clean_new_nickname(self):
        new_nickname = self.cleaned_data.get('new_nickname','').strip()
        if new_nickname == '':
            raise forms.ValidationError('新的昵称不能为空')
        return new_nickname

class BindEmailForm(forms.Form):
    email = forms.EmailField(label='邮箱',widget=forms.EmailInput(
                                attrs={'class':'form-control'}))
    verification_code = forms.CharField(label='验证码',required=False,widget=forms.TextInput(
                                attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录')

        # 判断用户是否已绑定邮箱
        if self.request.user.email != '':
            raise forms.ValidationError('你已经绑定邮箱')

        # 判断验证码
        code = self.request.session.get('bind_email_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经被绑定')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='旧的密码',widget=forms.PasswordInput(
                                attrs={'class':'form-control'}))
    new_password = forms.CharField(label='新的密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    new_password_again = forms.CharField(label='再次输入密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    #验证旧密码是否正确
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password','')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧密码输入错误')
        return old_password

    def clean_new_password_again(self):
        new_password = self.cleaned_data['new_password']
        new_password_again = self.cleaned_data['new_password_again']
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError('两次输入的密码不一致')
        return new_password_again

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    verification_code = forms.CharField(label='验证码', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    new_password = forms.CharField(label='新的密码',widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('email不存在')
        return email
    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')

        code = self.request.session.get('forgot_password_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return verification_code