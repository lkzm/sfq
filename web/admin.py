from django.contrib import admin
from .models import Profile, Track, Podcast, Series, Station, Queue, QTrack
admin.site.register(Profile)
admin.site.register(Track)
admin.site.register(Podcast)
admin.site.register(Series)
admin.site.register(Station)
admin.site.register(Queue)
admin.site.register(QTrack)
# Register your models here.
