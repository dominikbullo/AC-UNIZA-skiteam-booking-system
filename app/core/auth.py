from django.conf.urls import url
from django.urls import path, include
from django.views.generic import TemplateView

from users.api.views import FacebookLogin, ConfirmEmailView

urlpatterns = [

    path("", include('rest_auth.urls')),
    path("register/", include('rest_auth.registration.urls')),

    # FIXME Forgot passs
    url(r'^', include('django.contrib.auth.urls')),
    # TODO Forgot & Password reset via front
    # https://github.com/anexia-it/django-rest-passwordreset

    # Social
    path('facebook/', FacebookLogin.as_view(), name='fb_login'),
    # path('google/', GoogleLogin.as_view(), name='goggle_login')
]
