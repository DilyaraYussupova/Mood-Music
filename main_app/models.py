from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Playlist(models.Model):
    MOOD = (
        ('h', 'Happy'),
        ('s', 'Sad'),
        ('n', 'Nostalgic'),
        ('s', 'Sleepy'),
        ('e', 'Excited'),
    )
    description = models.TextField(max_length=300)
    mood = models.CharField(
        max_length=1,
        choices=MOOD,
        default=MOOD[0][0]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('playlist_list')