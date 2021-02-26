
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from web import forms
from web import models
import os
from django.contrib.auth.decorators import login_required, user_passes_test
from sfq import settings

def player(request):
    return render(request, 'web/player/index.html')


@login_required
def upload_track(request):
    form = forms.UploadTrackForm(request.POST, request.FILES)
    context = {
            'form' : form,
            }
    if form.is_valid():
        n = form.cleaned_data['name']
        a = form.cleaned_data['artist']
        f = form.cleaned_data['track']
        g = form.cleaned_data['genre']
        t = models.Track.objects.create(
                name = n,
                artist = a,
                genre = g,
                track = f
                )
        return track(request, t.pk)
    else:
        return render(request, 'web/radio/upload_track.html', context)
    return render(request, 'web/radio/upload_track.html', context)

def track (request, track_id):
    t = models.Track.objects.get(pk = track_id)
    context = {
            'name' : t.name,
            'track' : t.track,
            'genre' : t.genre,
            'artist' : t.artist,
            }
    return render(request, 'web/radio/trackid.html', context)


@login_required
def create_podcast (request, track_id, s_id):
    s = models.Series.objects.get(pk = s_id)
    t = models.Track.objects.get(pk = track_id)
    f = forms.CreatePodcastForm (request.POST, request.FILES)
    context = {
            'form':f,
            }
    if f.is_valid():
        p = f.cleaned_data['pic']
        a = f.cleaned_data['artist']
        pc = models.Podcast.objects.create(
                series = s,
                track = t,
                pic = p,
                number = s.episodes + 1, 
                artist = a
                )
        s.episodes = s.episodes + 1
        s.save()
        return podcast(request, pc.pk)
    else:
        return render(request, 'web/radio/create_podcast.html', context)
    return render(request, 'web/radio/create_podcast.html', context)

def podcast(request, podcast_id):
    p = models.Podcast.objects.get(pk = podcast_id)
    n = p.series.prefix + " " + str(p.number)
    context = {
            'name' : n,
            'pic' : p.pic,
            'track' : p.track.track,
            'artist' : p.artist,
            }
    return render(request, 'web/radio/podcastid.html', context)

def series_page(request):
    s = models.Series.objects.all()
    context = { 
            'series' : s,
            }
    return render(request, 'web/radio/series_page.html', context)

def series(request, s_id):
    s = models.Series.objects.get(pk = s_id)
    p = models.Podcast.objects.filter(series__pk = s_id)
    
    context = {
            'series' : s,
            'podcasts' : p,
            }
    return render(request, 'web/radio/seriesid.html', context)

def add_episode(request, s_id):
    s = models.Series.objects.get(pk = s_id)
    t = models.Track.objects.all()
    context = {
            'series' : s,
            'tracks' : t,
            }
    return render(request, 'web/radio/add_episode.html', context)
def create_station(request):
    if (request.method == 'POST'):
        f = forms.CreateStationForm(request.POST)
        n = f.cleaned_data('name')
        t = 0
        h = "34.91.84.7"
        p = "8000"
        st = models.Station.objects.create(t_num = t, name = n)
        st.mount = "sfq%"+str(st.pk)
        st.hostname = h
        st.port = p
        st.save()
        q = models.Queue.objects.create(np = 0, station = st, end=0)
        return add_tracks_queue(request, q.pk)
    else:
        f = forms.CreateStationForm()
        context = {
                'form' : f,
                } 
        return render(request, 'web/radio/create_station.html', context)



def next_in_queue(request, st_mount):
    st = models.Station.objects.get(mount = st_mount)
    q = models.Queue.objects.get(station__pk = st.pk)
    if q.end == 0:
        return HttpResponse("no queue active")
    elif q.np == q.end:
        num = 1
        qt = models.QTrack.objects.get(queue__pk = q.pk, numinq=num)
        text = "/home/vnubis.lkz/django/sfq/"+str(qt.track.track)+"/"
        return HttpResponse(text)
    else:
        num = q.np + 1
        qt = models.QTrack.objects.get(queue__pk = q.pk, numinq=num)
        text = "/home/vnubis.lkz/django/sfq/"+str(qt.track.track)+"/"
        return HttpResponse(text)
    
def play_next(request, st_mount):
    st = models.Station.objects.get(mount = st_mount) 
    q = models.Queue.objects.get(station__pk = st.pk)
    if q.end == 0:
        return HttpResponse("no queue active")
    elif q.np == q.end:
        num = 1
        q.np = 1
        q.save()
        qt = models.QTrack.objects.get(queue__pk = q.pk, numinq=num)
        text = "/home/vnubis_lkz/django/sfq/"+str(qt.track.track)
        return HttpResponse(text)
    else:    
        num = q.np + 1
        q.np = q.np +1
        q.save()
        qt = models.QTrack.objects.get(queue__pk = q.pk, numinq=num)
        text = "/home/vnubis_lkz/django/sfq/"+str(qt.track.track)
        return HttpResponse(text)

def add_track_queue(request, q_id, track_id):
    t = models.Track.objects.get(pk = track_id)
    q = models.Queue.objects.get(pk = q_id)
    tq = models.QTrack.objects.create(track = t, queue = q, numinq = q.end + 1)
    q.end = q.end + 1
    q.save()
    return edit_q(request, q_id)
def add_series_queue(request, s_id, q_id):
    ps = models.Podcast.objects.filter (series__pk = s_id)
    q = models.Queue.objects.get(pk = q_id) 
    for x in ps:
        tq = models.QTrack.objects.create(track = x.track, queue = q, numinq = q.end + 1)
        q.end = q.end + 1
        q.save()
    return edit_q(request, q_id)
def edit_q(request, q_id):
    qt = models.QTrack.objects.filter(queue__pk = q_id)
    t = models.Track.objects.all()
    sr = models.Series.objects.all()
    context = {
            'qt' : qt,
            'tracks' : t,
            'series' : sr,
            }
    return render(request, 'web/pleb/edit_q.html', context)










    
#def start (request, station_id):
#    station = models.Station.objects.get(pk = station_id)
#    playlist = station.playlist
#    files = []
#    for x in station.playlist.tracks:
#        t = x
#        t.file


