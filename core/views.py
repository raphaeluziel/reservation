from django.shortcuts import render

from django.http import HttpResponse,Http404
from django.http import JsonResponse
from django.db import models

# Create your views here.
def shift_detail(request,shift_id):
	return HttpResponse("hello this is shift detail page")

def index(request):

	return render(request, 'index.html')



def error_404_view(request, exception):
	return render(request, 'core/404.html')