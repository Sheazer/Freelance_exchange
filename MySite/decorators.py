from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView


def role_required(required_role):
    def decorator(view_func):
        def _wrapper_view(request, *args, **kwargs):
            if request.user.role == required_role:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have permission to access this page.")

        return _wrapper_view

    return decorator


def anonymous_required(function=None):
    decorator = user_passes_test(
        lambda user: not user.is_authenticated,
        login_url='/')
    if function:
        return decorator(function)
    return decorator
