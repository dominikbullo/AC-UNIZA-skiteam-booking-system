from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/rest-auth/", include("core.auth")),
    path("api/", include("config.api")),
]
