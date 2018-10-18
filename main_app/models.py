from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

MOODS = (
    ('h', 'Happy'),
    ('s', 'Sad'),
    ('p', 'Sleepy'),
    ('e', 'Emotional'),
)

# Create your models here.
class Song(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    year = models.IntegerField()
    photo_url = models.CharField(max_length=200, default='https://cdn.shopify.com/s/files/1/0638/5445/products/Chicago.jpg?v=1487360969')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/playlist_list/{self.mood}"

class Playlist(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(
        max_length=1,
        choices=MOODS,
        default=MOODS[0][0]
    )
    songs = models.ManyToManyField(Song, blank=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f"/playlist_list/{self.mood}"


