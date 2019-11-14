from django.shortcuts import redirect
from django.urls import path, include

from allauth.account.views import SignupView

# TODO: email registration
# https://django-registration.readthedocs.io/en/3.0/activation-workflow.html
from django_registration.backends.one_step.views import RegistrationView

# https://wsvincent.com/django-login-with-email-not-username/

urlpatterns = [
    # Login via browser
    path("", include('allauth.urls')),

    # Duplicating reg url -> there are /register and /signup
    path('register/', SignupView.as_view(), name="register"),

    # Login via browsable api
    path("api-auth/", include("rest_framework.urls")),

    # Login via REST
    path("api/rest-auth/", include("rest_auth.urls")),

    # # Registration via REST
    # path("api/rest-auth/signup/", include("rest_auth.registration.urls")),
]
