from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from re import compile

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'user')
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                path = request.get_full_path()
                return redirect_to_login(path, settings.LOGIN_URL, REDIRECT_FIELD_NAME)
