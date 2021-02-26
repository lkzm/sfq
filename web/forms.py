from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class SignUpForm(UserCreationForm):
    name = forms.CharField (max_length = 30, required = True, help_text = 'Name')
    email = forms.EmailField (max_length = 254, help_text = 'Required. Inform a valid email address.')
    bio = forms.CharField (max_length = 500, required = False, help_text = 'Optional')

    class Meta:
        model = User
        fields = ('username', 'name', 'bio', 'email', 'password1', 'password2', )



class UploadTrackForm(forms.Form):
    track = forms.FileField()
    name = forms.CharField(max_length = 255)
    artist = forms.CharField(max_length = 255)
    genre = forms.CharField(max_length = 255)

class CreatePodcastForm(forms.Form):
    pic = forms.ImageField()
    artist = forms.CharField(max_length = 255)


