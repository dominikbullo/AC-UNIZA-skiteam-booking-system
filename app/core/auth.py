from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("", include('rest_auth.urls')),
    path("register/", include('rest_auth.registration.urls')),
]
