from django.db import models
from django.conf import settings

class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    is_reminded = models.BooleanField(default=False)

    def __str__(self):
        return self.title
