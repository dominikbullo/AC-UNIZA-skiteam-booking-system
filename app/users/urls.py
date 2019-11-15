from django.conf.urls import url
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from allauth.account.views import SignupView

# https://django-registration.readthedocs.io/en/3.0/activation-workflow.html
# https://wsvincent.com/django-login-with-email-not-username/

urlpatterns = [
    # Login via browser
    path("", include('allauth.urls')),

    # Login via browsable api
    path("api-auth/", include("rest_framework.urls")),

    # Login via REST
    path("api/rest-auth/", include("rest_auth.urls")),

    # Registration via REST
    path("api/rest-auth/signup/", include("rest_auth.registration.urls")),

    # url(r'^api-token-auth/', obtain_auth_token)
]
