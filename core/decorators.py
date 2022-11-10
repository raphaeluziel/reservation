from django.shortcuts import redirect
from functools import wraps
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied


def user_not_authenticated(function=None, redirect_url='404.html'):
    """
    Decorator for views that checks that the user is NOT logged in, redirecting
    to the homepage if necessary by default.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
                
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator


def admin_staff_employer_required(view_func):
    def wrap(request, *args, **kwargs):
               
        if request.user.is_employer or request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('login'))
    return wrap


def admin_staff_nurse_required(view_func):
    def wrap(request, *args, **kwargs):
               
        if request.user.is_nurse or request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('login'))
    return wrap



def employer_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_employer:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('login'))
    return wrap
        

def staff_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('login'))
    return wrap



