from django.db import models
from django.utils import timezone

# Create your models here.
class LogEntry(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    source = models.CharField(max_length=100, blank=True, null=True)
    level = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"[{self.timestamp}] [{self.level}] [{self.source}] {self.message[:50]}"

    class Meta:
        ordering = ['-timestamp']
