from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100)
    points = models.IntegerField(default=0)
    url = models.URLField(default='')
    available = models.BooleanField(default=True)
    image_url = models.URLField(default='')
    link_url = models.URLField(default='')
    description = models.TextField(default='')
    stock = models.IntegerField(default=0)
    last_seen = models.DateTimeField(default=timezone.now)
    is_new = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class CronJobLog(models.Model):
    cron_id = models.CharField(max_length=100)
    executed_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Cron Job {self.cron_id} executed at {self.executed_at}"
