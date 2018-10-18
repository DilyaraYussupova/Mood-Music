from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import LoginForm
from .models import MOODS, Playlist, Song
from django.http import HttpResponseRedirect
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'moodmusicapp'

# Create your views here.
def home(request):
  return render(request, 'home.html')

def playlist_detail(request, mood):
    playlist = Playlist.objects.get(user=request.user, mood=mood)
    return render(request, 'playlist/detail.html', {'playlist': playlist})

class PlaylistListView(ListView):
    template_name = 'playlist/list.html'
    def get_queryset(self):
        return self.request.user.playlist_set.all()

class SongCreate(CreateView):
    model = Song
    fields = ['name', 'artist', 'album', 'genre', 'year']
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save()
        playlist = Playlist.objects.get(id=self.kwargs['pk'])
        playlist.songs.add(self.object)
        photo_file = self.request.FILES.get('photo-file', None)
        if photo_file:
            s3 = boto3.client('s3')
            # need a unique "key" for S3 / needs image file extension too
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            # just in case something goes wrong
            try:
                s3.upload_fileobj(photo_file, BUCKET, key)
                # build the full url string
                url = f"{S3_BASE_URL}{BUCKET}/{key}"
                self.object.photo_url = url
                self.object.save()
            except:
                print('An error occurred while uploading file to S3')
        return redirect(f"/playlist/{playlist.mood}")

class SongUpdate(UpdateView):
    model = Song
    template_name = 'main_app/song_update.html'
    fields = ['name', 'artist', 'album', 'genre', 'year']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        playlist = Playlist.objects.get(id=self.kwargs['playlist_id'])
        self.object.save()
        return redirect(f"/playlist/{playlist.mood}")

class SongDelete(DeleteView):
    model = Song
    template_name = 'main_app/song_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        playlist = Playlist.objects.get(id=self.kwargs['playlist_id'])
        self.object.delete()
        return redirect(f"/playlist/{playlist.mood}")

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            for mood in MOODS:
                playlist = Playlist(user=user, name=f"{mood[1]} Playlist", mood=mood[0])
                playlist.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    print("The account has been disabled.")
            else:
                print("The username and/or password is incorrect.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def add_photo(request, playlist_id):
	# photo-file was the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, playlist_id=playlist_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', playlist_id=playlist_id)