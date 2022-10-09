from django.shortcuts import get_object_or_404,render,redirect,HttpResponseRedirect

from django.http import HttpResponse,Http404
from django.http import JsonResponse
from django.db import models
from .models import CustomUser,Shift,Employer,AddressBook,CustomUserManager

from django.contrib.auth.forms import  SetPasswordForm, PasswordResetForm



from django.contrib.auth import authenticate, login,logout
from django import forms
from .forms import forms,CustomUserCreationForm,LoginForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages 

from django.contrib.auth import login, logout,authenticate 
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


from django.contrib.auth.forms import AuthenticationForm 



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
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
    
    return render(request, "login.html", {"form": form, "msg": msg})




def logout_view(request):
	logout(request)
	return render(request, 'index.html')





