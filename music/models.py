from django.db import models

# Create your models here.


class LastPlayedAudio(models.Model):
    audio_id = models.CharField(max_length=300, null=False)
    title = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=400, null=False)
    stream_url = models.CharField(max_length=2000, null=False)
    thumbnail = models.CharField(max_length=300, default=None, null=True)
