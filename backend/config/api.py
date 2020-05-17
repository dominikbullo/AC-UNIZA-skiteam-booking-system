from django.conf.urls import include
from django.urls import path

from core import router as custom_router

from apps.events.api.urls import router as events_router
from apps.family.api.urls import router as family_router
from apps.users.api.urls import router as user_router

router = custom_router.DefaultRouter()
router.extend(user_router)
router.extend(family_router)
router.extend(events_router)

# Settings
router.trailing_slash = '/?'

urlpatterns = [

    # Used for avatar
    path("", include("apps.users.api.urls")),

    # Not used, but good practice
    path("", include("apps.family.api.urls")),
    path("", include("apps.events.api.urls")),

    path("", include(router.urls)),
]
