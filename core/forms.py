from django.contrib.auth.forms import UserCreationForm, UserChangeForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.forms import widgets,ModelForm

from .models import Shift

from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django import forms
from django.conf import settings
import datetime

from django.utils import timezone
from datetime import datetime, date, time, timedelta
 

now = timezone.now()
import pytz
#from datetime import datetime, timedelta



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


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.DateInput):
    input_type = 'time'



class ShiftForm(ModelForm):
    class Meta:
        model = Shift
        fields = '__all__'

        widgets = {

            'shift_start_date': DateInput(),
            'shift_end_date': DateInput(),
            'start_time':TimeInput(),
            'finish_time':TimeInput(),
        }


    def clean(self):
            cleaned_data = super(ShiftForm,self).clean()
            shift_start_date = cleaned_data['shift_start_date']
           
            start_time = cleaned_data['start_time']
            finish_time = cleaned_data['finish_time']


            #current_date =datetime.now(tz=pytz.timezone('UTC'))

            current_date =datetime.now()
            
            if shift_start_date is not None and shift_start_date < current_date.date():   
                raise ValidationError("""shift start date should not be ealier than current_date""")
            #this one does not work

            elif shift_start_date == current_date and start_time.strftime<now:

                raise ValidationError("""start_time can not be ealier than current_time""")
               
            elif finish_time is not None and finish_time <= start_time : 
                #if shift_end_date is None:
                raise ValidationError("finish_time can not be earlier than or equal to start time") 
            else:

                return cleaned_data

    




   