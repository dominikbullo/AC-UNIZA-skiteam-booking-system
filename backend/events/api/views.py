from rest_framework import viewsets, generics, status, mixins
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

# from events.models import SkiTraining
# from events.api.serializers import EventSerializer
# from events.api.permissions import IsOwnerOrReadOnly, IsOwnFamilyOrReadOnly
#
#
# # https://github.com/LondonAppDeveloper/recipe-app-api/blob/master/app/recipe/views.py
# class EventsViewSet(viewsets.ModelViewSet):
#     queryset = SkiTraining.objects.all()
#     serializer_class = EventSerializer
#     # permission_classes = [IsOwnFamilyOrReadOnly]
#     # filter_backends = [SearchFilter]
#     # search_fields = ["name"]
#     pass
