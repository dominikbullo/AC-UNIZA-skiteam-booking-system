from django.contrib import admin
from django.urls import path, include, re_path

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
    path('admin/', admin.site.urls),
    path('', IndexTemplateView.as_view(), name="entry-point"),

    path("accounts/", include('allauth.urls')),

    # Login via REST
    path("api/rest-auth/", include("rest_auth.urls")),

    # # Registration via REST
    # path("api/rest-auth/signup/", include("rest_auth.registration.urls")),

    path("api/", include(router.urls)),

    path("api/", include("users.api.urls")),
    path("api/", include("family.api.urls")),
    path("api/", include("events.api.urls")),

    # everything else go to IndexTemplateView aka index.html od dev index page
    re_path(r"^.*$", IndexTemplateView.as_view(), name="entry-point")
]
from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
