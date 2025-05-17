from django.db import models
from django.utils import timezone

from django.db import models

class Visitor(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=200)
    path = models.CharField(max_length=100)
    is_new = models.BooleanField(default=True)
    
class DetectionLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    files_detected = models.JSONField()
    processes_detected = models.JSONField()
    scan_duration = models.FloatField()
    system_info = models.JSONField()

    def __str__(self):
        return f"Detection at {self.timestamp}"