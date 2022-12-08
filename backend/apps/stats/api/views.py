from django_filters import rest_framework as filters
from rest_framework import viewsets

from apps.events.models import Season
from apps.stats.api.serializers import ProfileStatSerializer, StatisticPolymorphicSerializer
from apps.stats.models import Statistic
from apps.users.models import Profile
from core.views import get_object_custom_queryset


def departments(request):
    if request is None:
        return Season.objects.none()

    return Season.objects.all()


# # RES: https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html#adding-a-filterset-with-filterset-class
# class StatsFilter(filters.FilterSet):
#     season = filters.ModelChoiceFilter(queryset=Season.objects.all())
#
#     class Meta:
#         model = Profile
#         fields = ("season", "user_role",)

# TODO: Simpler read only view
class ProfileStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing or retrieving statistic of events.
    For now only working with Child instances.
    """

    # TODO: When adding new feature disable filter
    queryset = Profile.objects.all()
    serializer_class = ProfileStatSerializer
    # TODO: Think about season filtering
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("user_role",)
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = StatsFilter


class StatsViewSet(viewsets.ModelViewSet):
    serializer_class = StatisticPolymorphicSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (
        "season",
        "user",
    )

    def get_queryset(self):
        return get_object_custom_queryset(self.request, Statistic)
