from django.contrib.auth import get_user_model
from rest_framework import serializers
from events.models import SkiTraining


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkiTraining
        fields = "__all__"
