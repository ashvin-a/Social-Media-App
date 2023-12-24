"""Middleware for group permission"""
from typing import List
from django.http import HttpResponse

def allowed_users(allowed_roles: List[str] = []):
    """Decorator function for group permission"""
    def decorator(view):
        def wrapper_fun(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page!')
        return wrapper_fun
    return decorator
