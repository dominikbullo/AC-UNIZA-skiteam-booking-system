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

from core import router
from core.views import IndexTemplateView

from users.api.urls import router as user_router
from family.api.urls import router as family_router

router = router.DefaultRouter()
router.extend(user_router)
router.extend(family_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexTemplateView.as_view(), name="entry-point"),

    path("account/", include('allauth.urls')),

    # Login via REST
    path("api/rest-auth/", include("rest_auth.urls")),

    # # Registration via REST
    # path("api/rest-auth/signup/", include("rest_auth.registration.urls")),

    path("api/", include(router.urls)),
    
    path("api/", include("users.api.urls")),
    path("api/", include("family.api.urls")),

    # everything else go to IndexTemplateView aka index.html od dev index page
    # re_path(r"^.*$", IndexTemplateView.as_view(), name="entry-point")
]
from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
