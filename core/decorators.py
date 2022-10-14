from django.shortcuts import redirect
from functools import wraps
from django.http import HttpResponse



def allowed_users(view, redirect_to='/'):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(redirect_to)
        else:
            return view(request, *args, **kwargs)
    return wrapper
