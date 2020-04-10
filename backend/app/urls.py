"""backend URL Configuration

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
from django.urls import path, re_path, include

from core import router
from core.views import IndexTemplateView

from users.api.urls import router as user_router
from family.api.urls import router as family_router
from events.api.urls import router as events_router

router = router.DefaultRouter()
router.extend(user_router)
router.extend(family_router)
router.extend(events_router)

urlpatterns = [
    # PWA needs to be first
    path("", IndexTemplateView.as_view(), name="entry-point"),
    path("", include('pwa.urls')),

    path("api/rest-auth/", include('core.auth')),

    path('admin/', admin.site.urls),

    # RELEASE: Delete or just admin only
    path('api/', include(router.urls)),

    path("api/", include("users.api.urls")),
    path("api/", include("family.api.urls")),
    path("api/", include("events.api.urls")),

    re_path(r'^\S+$', IndexTemplateView.as_view(), name="entry-point")
]
