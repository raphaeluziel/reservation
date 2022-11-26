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
 
import pytz
import bootstrap_datepicker_plus
from bootstrap_datepicker_plus.widgets import DatePickerInput,DateTimePickerInput
#from multiselectfield.forms.fields import MultiSelectFormField #added https://stackoverflow.com/questions/27332850/django-multiselectfield-cant-install



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
        fields=['first_name','last_name','email','phone','bios','date_joined']
        exclude = ['date_joined']


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.DateInput):
    input_type = 'time'



class CreateShiftForm(ModelForm):
    
    class Meta:
        model = Shift
        fields = '__all__'
        
        #fields=['nurse','employer','address','status','role','user','start_time','finish_time','details','published']
    

        widgets = {
             
                'start_time': DateTimePickerInput(),
                'finish_time':DateTimePickerInput(),

            }

    def clean(self):  

            cleaned_data = super().clean()
        
            start_time = cleaned_data['start_time']
            finish_time = cleaned_data['finish_time']
            now = timezone.now()
            current_date =datetime.now() 
          
            if start_time is not None and start_time < now:
                raise ValidationError("shift time should not be ealier than current_date,time")
            
            elif start_time == finish_time:
                raise ValidationError("Your finish time is equal to start time")

            elif finish_time <start_time:
                raise ValidationError("The finish time can not be ealier than the start time")       
            else:
                return cleaned_data



class ReserveShiftForm(ModelForm):
    
    class Meta:
        model = Shift
        fields = '__all__'
        exclude=['employer','address','is_published','details','status','user','shift_date']
        
        widgets = {
                'shift_date': DatePickerInput(),
                'start_time': DateTimePickerInput(),
                'finish_time':DateTimePickerInput(),

            }
        def clean(self):  

            cleaned_data = super().clean()
            #shift_date = cleaned_data['shift_date']
            start_time = cleaned_data['start_time']
            finish_time = cleaned_data['finish_time']
            
           
            return cleaned_data



class UpdateShiftForm(ModelForm):
    
    class Meta:
        model = Shift
        fields = '__all__'
        

        widgets = {
                'shift_date': DatePickerInput(),
                'start_time': DateTimePickerInput(),
                'finish_time':DateTimePickerInput(),

            }

    def clean(self):  

            cleaned_data = super().clean()
            shift_date = cleaned_data['shift_date']
            start_time = cleaned_data['start_time']
            
            if shift_date!=start_time.date():
                raise ValidationError("Please recheck and make sure that shift date and shift start time date are the same")
              
            else:
                return cleaned_data


   