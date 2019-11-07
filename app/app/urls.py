"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django_registration.backends.one_step.views import RegistrationView

from users.forms import CustomUserCreationForm

# TODO: email registration
# https://django-registration.readthedocs.io/en/3.0/activation-workflow.html


urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom registration via browser
    path("accounts/register/",
         RegistrationView.as_view(
             form_class=CustomUserCreationForm,
             success_url="/",
         ), name="django_registration_register"),

    # other url's used by django registration package
    path("accounts/", include("django_registration.backends.one_step.urls")),

    # Login via browser
    path("accounts/", include("django.contrib.auth.urls")),

    # Login via browsable api
    path("api-auth/", include("rest_framework.urls")),

    # Login via REST
    path("api/rest-auth/", include("rest_auth.urls")),

    # Registration via REST
    path("api/rest-auth/registration/", include("rest_auth.registration.urls")),
]

from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
