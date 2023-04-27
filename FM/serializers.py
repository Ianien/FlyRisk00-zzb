from rest_framework import serializers
from .models import FlyTask


class FlyTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlyTask
        fields = "__all__"
