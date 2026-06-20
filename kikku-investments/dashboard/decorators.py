from functools import wraps

from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect


def active_user_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        if request.user.status == "blocked":
            messages.error(
                request,
                "Your account has been blocked."
            )
            logout(request)
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper
