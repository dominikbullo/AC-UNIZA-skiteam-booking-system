from rest_framework.routers import DefaultRouter

from apps.stats.api.views import ProfileStatsViewSet, StatsViewSet

app_name = "stats"

# https://www.django-rest-framework.org/api-guide/routers/
router = DefaultRouter()
router.register(r"stats?", StatsViewSet, basename="stats")
router.register(r"profile-stats?", ProfileStatsViewSet, basename="profile-stats")
