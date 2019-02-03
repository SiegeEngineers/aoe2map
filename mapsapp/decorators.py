from functools import wraps

from django.http import JsonResponse


def ajax_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return JsonResponse({'not_authenticated': True}, status=403)
    return wrapper
