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
from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter

from users.api.views import ProfileViewSet

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", include('allauth.urls')),

    # Login via REST
    path("api/rest-auth/", include("rest_auth.urls")),
    path("api/profiles/", include("users.api.urls")),

    # # Registration via REST
    # path("api/rest-auth/signup/", include("rest_auth.registration.urls")),

    path("api/user/", include("users.api.urls")),
    path("api/family/", include("family.api.urls")),

    # FAMILY
    # path("family/", include("family.urls")),
    # path("api/family/", include("family.api.urls")),

    # everything else go to IndexTemplateView aka index.html od dev index page
    # re_path(r"^.*$", IndexTemplateView.as_view(), name="entry-point")
]

from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
