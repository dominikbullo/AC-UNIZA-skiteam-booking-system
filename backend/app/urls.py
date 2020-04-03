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
from core.views import serve_worker_view, index_view

from users.api.urls import router as user_router
from family.api.urls import router as family_router
from events.api.urls import router as events_router

router = router.DefaultRouter()
router.extend(user_router)
router.extend(family_router)
router.extend(events_router)

urlpatterns = [
    # http://localhost:8000/
    path('', index_view, name='index'),

    # http://localhost:8000/admin/
    path('admin/', admin.site.urls),
    
    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),

    # serve static files for PWA
    path('index.html', index_view, name='index'),
    re_path(r'^(?P<worker_name>manifest).json$', serve_worker_view, name='manifest'),
    re_path(r'^(?P<worker_name>[-\w\d.]+).js$', serve_worker_view, name='serve_worker'),
    re_path(r'^(?P<worker_name>robots).txt$', serve_worker_view, name='robots'),

    path("api/rest-auth/", include('core.auth')),

    path("api/", include("users.api.urls")),
    path("api/", include("family.api.urls")),
    path("api/", include("events.api.urls")),

    # support vue-router history mode
    re_path(r'^\S+$', index_view, name='SPA_reload'),
]
