from django.shortcuts import get_object_or_404,render,redirect,HttpResponseRedirect

from django.http import HttpResponse,Http404,JsonResponse

from django.db import models
from .models import CustomUser,Shift,Employer,AddressBook,CustomUserManager

from django.contrib.auth.forms import  SetPasswordForm, PasswordResetForm,AuthenticationForm 
from django.contrib.auth import authenticate, login,logout,get_user_model,password_validation
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.hashers import make_password
from django.contrib import messages 
from django.contrib.auth.decorators import login_required

from .decorators import allowed_users

from django import forms
from .forms import forms,CustomUserCreationForm,LoginForm,ChangePasswordForm

from django.core.mail import send_mail, BadHeaderError
from django.utils.http import urlsafe_base64_encode
from django.conf import settings




# Create your views here.
def shift_detail(request,shift_id):
	return HttpResponse("hello this is shift detail page")

def index(request):

	return render(request, 'index.html')

def shift_detail(request,shift_id):
	shift=get_object_or_404(Shift, pk=shift_id)
	return render(request, 'shift_detail.html',{'shift':shift})

def shifts(request):
	shifts=Shift.objects.all().order_by('-pub_date')[:5]
	employers=Employer.objects.all()

	context={'shifts':shifts,'employers':employers}

	return render(request,'shifts.html',context)



def error_404_view(request, exception):
	return render(request, 'core/404.html')



def login_view(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
        	username = form.cleaned_data.get("email")
        	password = form.cleaned_data.get("password")
        	user = authenticate(request,username=username, password=password)
        	if user is not None:
        		login(request, user)
        		return redirect('/')
        	else:
        		error = 'Invalid Credentials'
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error': error})


def logout_view(request):
	logout(request)
	return render(request, 'index.html')


@login_required(login_url='login')

def password_reset_view(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            
            user.password = make_password(form.cleaned_data["new_password2"])
            user.save()
            messages.success(request, "Your password has been changed")
            return redirect('/')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = ChangePasswordForm()
    return render(request, 'password_reset.html', {'form': form})







