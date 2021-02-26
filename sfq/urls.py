"""sfq URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web import account, radio
from django.conf import settings
from django.conf.urls.static import static
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
 
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', account.signup, name='signup'),
    path('radio/', radio.player, name='player'),
    path('upload/', radio.upload_track, name = 'upload'),
    path('create_podcast%<int:s_id>%<int:track_id>/', radio.create_podcast, name ='create_podcast'),
    path('series_home/', radio.series_page, name = 'series_home'),
    path('series%<int:s_id>/',radio.series, name = 'series'),
    path('podcast%<int:podcast_id>/', radio.podcast, name = 'podcast'),
    path('track%<int:track_id>/', radio.track, name = 'track'),
    path('add_episode%<int:s_id>/', radio.add_episode, name = 'add_episode'),
    path('check_next%<str:st_mount>/', radio.play_next, name = 'play_next'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
