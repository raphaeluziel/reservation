from django.shortcuts import get_object_or_404,render

from django.http import HttpResponse,Http404
from django.http import JsonResponse
from django.db import models
from .models import CustomUser,Shift,Employer,AddressBook,CustomUserManager

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