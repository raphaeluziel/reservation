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
from django.shortcuts import redirect


def user_not_authenticated(function=None, redirect_url='/'):
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




def employer_only(view):
  @wraps(view)
  def wrapper(request, *args, **kwargs):

        if request.user.customuser.is_employer:
            return view(request, *args, **kwargs)
        else:
            return HttpResponse('<h1>You are not employer, not allowed access</h1>')
  return wrapper







