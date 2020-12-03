from django.urls import path
from django.contrib import admin


from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/rest-auth/", include('core.auth')),
    path('api/', include('config.api')),
]
