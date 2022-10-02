
from django.urls import path
from . import views
from .models import *



urlpatterns = [
    path('', views.index, name="index"),
    path('shifts/<int:shift_id>/',views.shift_detail,name="shift_detail"),
    path('shifts/',views.shifts, name="shifts"),

]

handler404='core.views.error_404_view'