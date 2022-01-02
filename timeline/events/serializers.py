from rest_framework import serializers
from timeline.events import models

class EventSerializer(serializers.ModelSerializer):
    start = serializers.DateField(source="date", read_only=True)

    class Meta:
        model = models.Event
        fields = ("id", "title", "icon", "date", "start")
        write_only_fields = ("date",)
        read_only_fields = ("start",) 
