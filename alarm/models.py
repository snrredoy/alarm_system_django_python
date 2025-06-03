from django.db import models


# Create your models here.
class Alarm(models.Model):
    user_id = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField()
    days = models.JSONField(default=list, blank=True, null=True)
    enabled = models.BooleanField(default=True)
    timezone = models.CharField(max_length=100, default='UTC')

    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.date:
            return f"Alarm at {self.time} on {self.date}"
        return f"Alarm at {self.time} repeating on {', '.join(self.days)}"


