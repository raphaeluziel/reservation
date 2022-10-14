
from django.urls import path
from . import views
from .models import *
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout



urlpatterns = [
    path('', views.index, name="index"),
    path('shifts/<int:shift_id>/',views.shift_detail,name="shift_detail"),
    path('shifts/',views.shifts, name="shifts"),
    path('login/',views.login_view, name="login"),
    path('logout/',views.logout_view, name="logout"),
    path('password_reset/', views.password_reset_view, name="password_reset"),

]

handler404='core.views.error_404_view'