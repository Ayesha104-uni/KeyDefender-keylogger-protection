from rest_framework import serializers
from .models import DetectionLog

class DetectionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectionLog
        fields = ['id', 'timestamp', 'files_detected', 'processes_detected', 'scan_duration', 'system_info']