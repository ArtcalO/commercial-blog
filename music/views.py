from django.shortcuts import  render, redirect, reverse, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, models

# Create your views here.

def musicList_view(request):
    musics = Music.objects.all()
    slides = Slides.objects.all()
    slide1 = slides[0]
    slides = slides[1:3]
    return render(request, 'music/acceuil_app.html', locals())

def payement_view(request, slug=None):
    form = PayementForm(request.POST or None)
    if not slug:
        musics = Music.objects.all()
        if form.is_valid():
            payement_method = form.cleaned_data['payement_method']
            amount = form.cleaned_data['amount']
            identification = form.cleaned_data['identification']
    else:
        musics = Music.objects.filter(slug=slug)

    return render(request, 'music/pay_download.html', locals())

def music_player_view(request, slug=None):
    if not slug:
        musics = Music.objects.all()
    else:
        musics = Music.objects.filter(slug=slug)

    return render(request, 'music/music_player.html', locals())


def about_music_view(request, slug=None):
    if not slug:
    	musics = Music.objects.all()
    else:
        musics = Music.objects.filter(slug=slug)

    return render(request, 'music/about_music.html', locals())


def login_view(request):
    error = False
    # next = request.GET["next"]
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(musicList_view)
            else:
                error = True
    else:
        form = LoginForm()

    return render(request, 'music/login.html', locals())

def logout_view(request):
    logout(request)
    return redirect(reverse(musicList_view))

def register(request):
    if request.method == 'POST':
        form = UserCreationForm()

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('music')
    else:
        form = UserCreationForm()

    context = {'form' : form}
    return render(request, 'music/register.html', context)