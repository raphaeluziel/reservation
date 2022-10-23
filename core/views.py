from django.shortcuts import get_object_or_404,render,redirect,HttpResponseRedirect

from django.http import HttpResponse,Http404,JsonResponse

from django.db import models
from django.db.models.query_utils import Q
from django.core.mail import EmailMessage
from .models import CustomUser,Shift,Employer,AddressBook,CustomUserManager

from django.contrib.auth.forms import  SetPasswordForm, PasswordResetForm,AuthenticationForm
from django.contrib.auth import authenticate, login,logout,get_user_model,password_validation
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages 
from django.contrib.auth.decorators import login_required

from .decorators import allowed_users,user_not_authenticated, is_customer

from django import forms
from .forms import forms,CustomUserCreationForm,LoginForm,PasswordResetForm,UserUpdateForm,ShiftForm

from django.core.mail import send_mail, BadHeaderError
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str

from django.conf import settings
from django.template.loader import render_to_string
from .tokens import account_activation_token


# Create your views here.


def index(request):

	return render(request, 'index.html')

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
        		messages.info(request, 'Username or Password is incorrect')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error': error})


def logout_view(request):
	logout(request)
	return render(request, 'index.html')

@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'password_reset_confirm.html', {'form': form})

@user_not_authenticated
def password_reset_view(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'password_reset_confirm.html', {'form': form})



@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )

                    return redirect('login')
                else:
                	messages.error(request,"something went wrong, wait some minutes and check again later")

            else:
                messages.error(request, "we did not find such a user.")
                  

            return redirect('password_reset_request')

        # for key, error in list(form.errors.items()):
        #     if key == 'captcha' and error[0] == 'This field is required.':
        #         messages.error(request, "You must pass the reCAPTCHA test")
        #         continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="password_reset_request.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("/")


@login_required

def profile(request, id):

	if request.method=="POST":
		user=request.user
		form=UserUpdateForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			user_form=form.save()
			messages.success(request, f'{user_form.firstname},your profile has been updated')
			return redirect("profile",user_form.firstname)
		for error in list(form.errors.values()):
			messages.error(request,error)
	user=get_user_model().objects.filter(id=id).first()
	if user:
		form=UserUpdateForm(instance=user)

		return render(
	 		request=request,
	 		template_name="profile.html",
	 		context={"form":form})
	return redirect("/")

@login_required
def shift_detail(request,shift_id):
	shift=get_object_or_404(Shift, pk=shift_id)
	return render(request, 'shift_detail.html',{'shift':shift})


@login_required
def shifts(request):
	employers=Employer.objects.all()
	shifts=Shift.objects.all().order_by('-pub_date')[:5]
	context={'shifts':shifts,'employers':employers}

	return render(request,'shifts.html',context)


### Create, Update, Delete, Pulish a draft shift part. Only employer /staff /admin have the access rights###

@login_required
def createShift(request):
	form = ShiftForm()
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = ShiftForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'shift_form.html', context)



def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def updateShift(request, pk):

	shift = Shift.objects.get(id=pk)
	form = ShiftForm(instance=shift)

	if request.method == 'POST':
		form = ShiftForm(request.POST, instance=shift)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'shift_form.html', context)

def deleteShift(request, pk):
	shift = Shift.objects.get(id=pk)
	if request.method == "POST":
		shift.delete()
		return redirect('/')

	context = {'shift':shift}
	return render(request, 'delete_shift.html', context)

# reserve one shift and then redirect to all reversed_shifts list view
@login_required #here employee reserves that offered jobs on job list
def reserve_shift(request, pk):
    
    shift = Shift.objects.get(id=pk)
    if request.method == 'POST':
        shift.user = request.user
        shift.time_reserved = datetime.datetime.now()
        shift.save()
    return redirect('reserved_shifts')


#list all reserved shifts by that employee


@login_required 
def reversed_shifts(request):
    shifts=Shift.objects.filter(user=request.user)
    context = {'reserved_shifts': shifts,}
    return render(request,'reserved_shifts.html', context=context)


def error_404_view(request, exception):
	return render(request, 'core/404.html')

