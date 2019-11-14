from django.contrib.auth import views as auth_views
from django.urls import path, include

from users import views as user_views

# TODO: email registration
# https://django-registration.readthedocs.io/en/3.0/activation-workflow.html
from django_registration.backends.one_step.views import RegistrationView

from users.forms import CustomUserCreationForm

# https://wsvincent.com/django-login-with-email-not-username/


urlpatterns = [
    # Login via browser
    path("", include('allauth.urls')),
    # path("", include("django.contrib.auth.urls")),

    path("api/", include("users.api.urls")),

    # Login via browsable api
    path("api-auth/", include("rest_framework.urls")),

    # Login via REST
    path("api/rest-auth/", include("rest_auth.urls")),

    # Registration via REST
    path("api/rest-auth/signup/", include("rest_auth.registration.urls")),
]
