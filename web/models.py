from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField (User, on_delete=models.CASCADE)
    bio = models.TextField (max_length = 500, blank = True)
    name = models.CharField (max_length = 30 , blank = True)


@receiver (post_save, sender=User)
def update_user_profile (sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()

class Series (models.Model):
    name = models.CharField (max_length = 255, default = "nonamed series")
    episodes = models.IntegerField (default = 0)
    prefix = models.CharField (max_length = 6, default = "noname")
    picture = models.ImageField(upload_to = 'files/image', default = 'files/image/default.jpg')

class Track (models.Model):
    name = models.CharField (max_length=255, default = "empty")
    artist = models.CharField (max_length = 255, default = "Angerfist")
    genre = models.CharField (max_length = 255, default = "electronic")
    track = models.FileField (upload_to = 'files/audio')
    
class Podcast (models.Model):
    series = models.ForeignKey(Series, on_delete = models.CASCADE)
    number = models.IntegerField (default = 0)
    artist = models.CharField (max_length = 255, default = "Angerfist")
    track = models.ForeignKey(Track, on_delete = models.CASCADE)
    pic = models.ImageField(upload_to = 'files/image', blank = True)
    
class Station (models.Model):
    name = models.CharField(max_length=255, blank=True)
    hostname = models.TextField(max_length=200, blank=True)
    port = models.TextField(max_length=10, blank=True)
    mount = models.TextField(max_length=255, blank=True)
    


class Queue (models.Model):
    np = models.IntegerField(default = 0)
    station = models.ForeignKey(Station, on_delete = models.CASCADE)
    end = models.IntegerField(default=0)

class QTrack (models.Model):
    track = models.ForeignKey(Track, on_delete = models.CASCADE)
    queue = models.ForeignKey(Queue, on_delete = models.CASCADE)
    numinq = models.IntegerField(default = 0)




    
    

# Create your models here.
