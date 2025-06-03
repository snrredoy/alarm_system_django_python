from rest_framework import serializers
from .models import Alarm

class AlarmSerializer(serializers.ModelSerializer):
    days = serializers.ListField(child=serializers.CharField(), required=False, default=[])

    class Meta:
        model = Alarm
        fields = ['id', 'user_id', 'date', 'time', 'days', 'enabled', 'is_active', 'timezone']

    def validate(self, data):
        if not data.get('date') and not data.get('days'):
            raise serializers.ValidationError("Either 'date' or 'days' must be provided.")
        return data