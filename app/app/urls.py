from django.contrib import admin
from django.urls import path, include, re_path

from core import router
from core.views import IndexTemplateView

from users.api.urls import router as user_router
from family.api.urls import router as family_router
from events.api.urls import router as events_router

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView)

router = router.DefaultRouter()
router.extend(user_router)
router.extend(family_router)
router.extend(events_router)

urlpatterns = [
    path('admin/', admin.site.urls),

    path("accounts/", include('allauth.urls')),

    # Token
    # https://github.com/davesque/django-rest-framework-simplejwt
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path("api/", include(router.urls)),

    path("api/", include("users.api.urls")),
    path("api/", include("family.api.urls")),
    path("api/", include("events.api.urls")),

    # everything else go to IndexTemplateView aka index.html od dev index page
    re_path(r"^.*$", IndexTemplateView.as_view(), name="entry-point"),
    path('', IndexTemplateView.as_view(), name="entry-point"),
]
from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
