from django.contrib.auth.forms import UserCreationForm, UserChangeForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.forms import widgets,ModelForm

from .models import Shift

from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django import forms
from django.conf import settings


#from users.models import OtpCode

from .models import *


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

from django import forms

class LoginForm(forms.Form):
    
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()

    class Meta:
        model=get_user_model()
        fields=['first_name','last_name','email','phone']


class ShiftForm(ModelForm):
    class Meta:
        model = Shift
        fields = '__all__'
 