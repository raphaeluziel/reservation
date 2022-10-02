
from django.urls import path
from . import views
from .models import *



urlpatterns = [
    path('', views.index, name="index"),

]

handler404='core.views.error_404_view'