from django.shortcuts import get_object_or_404,render,redirect,HttpResponseRedirect

from django.http import HttpResponse,Http404,JsonResponse

from django.db import models
from django.db.models import Q
#from django.db.models.query_utils import Q
from django.core.mail import EmailMessage
from .models import CustomUser,Shift,Employer,AddressBook,CustomUserManager,Nurse

from django.contrib.auth.forms import  SetPasswordForm, PasswordResetForm,AuthenticationForm
from django.contrib.auth import authenticate, login,logout,get_user_model,password_validation
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages 
from django.contrib.auth.decorators import login_required,user_passes_test

from .decorators import user_not_authenticated,admin_staff_employer_required,employer_only,staff_only

from django import forms
from .forms import forms,CustomUserCreationForm,LoginForm,PasswordResetForm,UserUpdateForm,ShiftForm

from django.core.mail import send_mail, BadHeaderError
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str

from django.conf import settings
from django.template.loader import render_to_string
from .tokens import account_activation_token
import datetime

from itertools import chain
from django.urls import reverse,reverse_lazy
import datetime
from datetime import datetime, timedelta


# Create your views here.

def landing(request):

	return render(request, 'landing.html')


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
        		return redirect("shifts")
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

def profile(request,id):

	if request.method=="POST":
		user=request.user
		form=UserUpdateForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			user_form=form.save()
			messages.success(request, f'{user_form.first_name},your profile has been updated')
			return redirect("profile",user_form.id)
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



def is_valid_queryparam(param):
    return param != '' and param is not None

@login_required
def shift_filter(request):
    user=request.user
    employer=Employer.objects.all()
    nurse = Nurse.objects.all()
    if request.user.is_employer:
    	qs = Shift.objects.all().filter(employer_id=user.id).order_by('-shift_start_date')[:5]
    else:
    	qs = Shift.objects.all()

    address_contains_query = request.GET.get('address_contains')
    org_name_contains_query = request.GET.get('org_name_contains')
    
    #id_exact_query = request.GET.get('id_exact')
    nurse_id_exact_query=request.GET.get('nurse_id_exact')
    role= request.GET.get('role') 
    print(role)
    status= request.GET.get('status')

    shift_start_date_min = request.GET.get('shift_start_date_min')
    shift_start_date_max = request.GET.get('shift_start_date_max')

   

    if is_valid_queryparam(address_contains_query):
        qs = qs.filter(address__city__icontains=address_contains_query)

    if is_valid_queryparam(org_name_contains_query):
        qs = qs.filter(employer__org_name__icontains=org_name_contains_query)

    if is_valid_queryparam(nurse_id_exact_query):
        qs = qs.filter(nurse=nurse_id_exact_query)

    if is_valid_queryparam(shift_start_date_min):
        qs = qs.filter(shift_start_date__gte=shift_start_date_min)

    if is_valid_queryparam(shift_start_date_max):
        qs = qs.filter(shift_start_date__lte=shift_start_date_max)

    if is_valid_queryparam(role) and role!='Choose...':
       qs = qs.filter(role=role)
    
    if is_valid_queryparam(status) and status != 'Choose...':
        qs = qs.filter(status=status)

    return qs


@login_required
def shifts(request):
	user=request.user
	employer=Employer.objects.all()
	qs=shift_filter(request)
	
	#print(Shift.objects)
	if request.user.is_employer:
	
	#if login user is an employer, then this employer could see only his/her own published shifts (not other employers')
	
		#e.g. in shell, query  was  print(Shift.objects.all().filter(employer_id=2))
		shifts=Shift.objects.all().filter(employer_id=user.id).order_by('-shift_date')[:5]
		


	#if user is admin, job agency staff or nurse, then all shifts are visible
	else:
		
		shifts=Shift.objects.all().order_by('shift_date')
	
	roles=Shift().ROLES 
	statuses=Shift().STATUS
	context={'shifts':shifts,'queryset':qs,'statuses':statuses,'roles':roles}

	return render(request,'shifts.html',context)


	"""
	In shifts view, one more condition between if and else
	elif request.user.is_nurse:
		if self.request.user.has_perm('register RN jobs then show all vacanies'):
    			# do this
		else:
   			 #show only Practical nurse or assistance vacancies

    """


### Create, Update, Delete, Pulish a draft shift part. Only employer /staff /admin have the access rights###
#to add if nurse, then it's not allowed to create shift

@login_required
def shift_detail(request,shift_id):
	shift=get_object_or_404(Shift, pk=shift_id)
	return render(request, 'shift_detail.html',{'shift':shift})

@login_required
@admin_staff_employer_required
def createShift(request):
	user=request.user
	employer=Employer.objects.all()
	form = ShiftForm()
	if request.method == 'POST':
		
		#print('Printing POST:', request.POST)
		form = ShiftForm(request.POST)
		if form.is_valid():

			if request.user.is_employer:
				employer=request.user
			form.save()
			messages.success(request, "The shift has been created")
			return redirect('/')
		else:
			print(form.errors)
			#form = ShiftForm()
			
			#messages.error(request,"something went wrong")

	context = {'form':form}
	return render(request, 'create_shift.html', context)


@login_required
def updateShift(request, pk):

	shift = Shift.objects.get(id=pk)
	form = ShiftForm(instance=shift)
	#shift_start_date=request.shift_start_date

	if request.method == 'POST':
		form = ShiftForm(request.POST, instance=shift)

		if form.is_valid():
			
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'create_shift.html', context)

@login_required
@admin_staff_employer_required
def deleteShift(request, pk):
	shift = Shift.objects.get(id=pk)
	if request.method == "POST":
		if request.user.is_employer and shift.status=="Reserved":
			messages.error(request,"This shift has already been reserved, please contact our customer service for further information.")
		else:
			shift.delete()
			return redirect('/')

	context = {'shift':shift}
	return render(request, 'delete_shift.html', context)


# reserve one shift and then redirect to all reversed_shifts list view
@login_required #here employee reserves that offered jobs on job list
def reserve_shift(request, pk):
    
    shift = Shift.objects.get(id=pk)
    if request.method == 'GET':
        shift.user = request.user #shift.reserved_by=request.user
        shift.status = 'Reserved'
        shift.time_reserved = datetime.datetime.now()
        shift.save()
        messages.success(request, "The shift has been reserved")
    return redirect('reserved_shifts')


#list all reserved shifts by that employee


@login_required 
def reversed_shifts(request):
    shifts=Shift.objects.filter(user=request.user)
    context = {'reserved_shifts': shifts}
    return render(request,'reserved_shifts.html', context=context)



@login_required


# search function

# case 1.

# 	If login_user=="employer", then the search result shows only user name and email. For instance, employer could find a nurse 
# 	quickly and add that nurse to both agreed shift. The employer could not however view other employers' shift info, etc.

# case 2.

# 	If login_user =="admin" or "staff " or "nurse", the user could search for avaible job place, employer org name, job details, etc. 


def search(request):

	user=request.user
	employers=Employer.objects.all()
	query = request.GET.get('query')
	if not query:
		return HttpResponse("Please input search text..")
	else:
		if request.user.is_employer:

		    results = CustomUser.objects.filter(
		         Q(last_name__icontains=query)| Q(first_name__icontains=query)|Q(email__icontains=query)
		    )

		else:

		    shift_results = Shift.objects.filter(
		         Q(role__icontains=query)| Q(details__icontains=query)| Q(address__city__icontains=query)
		    )
		    #print(type(shift_results))
		    customuser_results = CustomUser.objects.filter(
		         Q(last_name__icontains=query)| Q(first_name__icontains=query)|Q(email__icontains=query)
		    )

		    employer_results = Employer.objects.filter(
		         Q(org_name__icontains=query)
		    )
		    results= list(chain(shift_results, customuser_results,employer_results))#from itertools import chain
		    print(type(results))
		context={
		   	"results": results,
		    "query": query,

		    }
		
		return render(request, "search.html", context)


def error_404_view(request, exception):
	return render(request, 'core/404.html')


