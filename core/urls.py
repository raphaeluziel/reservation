
from django.urls import path
from . import views
from .models import *
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout



urlpatterns = [
    path('', views.index, name="index"),
    path('landing/', views.landing, name="landing"),
    path('shifts/<int:shift_id>/',views.shift_detail,name="shift_detail"),
    path('shifts/',views.shifts, name="shifts"),
    path('login/',views.login_view, name="login"),
    path('logout/',views.logout_view, name="logout"),
    path('password_change/', views.password_change, name="password_change"),
    path('password_reset_request/', views.password_reset_request, name="password_reset_request"),
    path('password_reset/', views.password_reset_view, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    path("profile/<id>/",views.profile, name="profile"),
    path('create_shift/', views.createShift, name="create_shift"),
    path('update_shift/<str:pk>/', views.updateShift, name="update_shift"),
    path('delete_shift/<str:pk>/', views.deleteShift, name="delete_shift"),
    path('reserved_shifts', views.reversed_shifts, name="reserved_shifts"),
    path('reserve_shift/<str:pk>/', views.reserve_shift, name="reserve_shift"),
    path('search/', views.search, name='search'),

]

handler404='core.views.error_404_view'