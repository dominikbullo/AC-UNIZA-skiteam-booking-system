from django.urls import path, include
from users.forms import CustomUserCreationForm

# TODO: email registration
# https://django-registration.readthedocs.io/en/3.0/activation-workflow.html
# from django_registration.backends.one_step.views import RegistrationView
from django_registration.views import RegistrationView

urlpatterns = [
    # Custom registration via browser
    path("accounts/register/",
         RegistrationView.as_view(
             form_class=CustomUserCreationForm,
             success_url="/",
         ), name="django_registration_register"),

    # other url's used by django registration package
    # path("accounts/", include("django_registration.backends.one_step.urls")),

    # Use 2 step verification
    path("accounts/", include('django_registration.backends.activation.urls')),

    # Login via browser
    path("accounts/", include("django.contrib.auth.urls")),

    # Login via browsable api
    path("api-auth/", include("rest_framework.urls")),

    # Login via REST
    path("api/rest-auth/", include("rest_auth.urls")),

    # Registration via REST
    path("api/rest-auth/registration/", include("rest_auth.registration.urls")),
]
