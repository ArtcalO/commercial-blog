from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.shortcuts import render
from .forms import *
from .models import Films, Avis, Commentaires, Achats
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def inscription_view(request):
    inscription = "S'inscrire"
    form_view_inscr = InscriptionForm(request.POST or None)
    if request.method == "POST":
        if form_view_inscr.is_valid():
            pseudo = form_view_inscr.cleaned_data['pseudo']
            mail = form_view_inscr.cleaned_data['email']
            pass1 = form_view_inscr.cleaned_data['password1']
            pass2 = form_view_inscr.cleaned_data['password2']
            if pass1 == pass2:
                User.objects.create_user(username = pseudo, email = mail, password = pass1)
                print("Votre compte a été créé aveec success!")
            else:
                print("Les mots de pass ne sont pas identiques!")

    return render(request, 'inscription.html', locals() )

def connexion_view(request):
    cone = "Se conncter"

    form_view_con = ConnexionForm(request.POST or None)
    if request.method == "POST":
        if form_view_con.is_valid():
            pseudo = form_view_con.cleaned_data['pseudo']
            pass1 = form_view_con.cleaned_data['password1']
            user = authenticate(username = pseudo, password = pass1)

            if user:
                login(request, user)
                print("Vous etes connecté!")
                return redirect(acceuil_app)
            else:
                connexion_msg = "Pseudo ou Mot de pass est incorrect !"

    else:
        form = ConnexionForm()

    return render(request, 'connection.html', locals() )

def deconnexion_view(request):
    logout(request)
    return redirect(acceuil_app)

def acceuil_app(request):
    acceuil = "Page d'acceuil"
    film_obj = Films.objects.all().order_by('date')
    page = request.GET.get('page', 1)          # page à charger par defaut
    paginator = Paginator(film_obj, 8)         # limiter tous les elements à afficher

    try:
        filmsPage = paginator.page(page)
    except PageNotAnInteger:
        filmsPage = paginator.page(1)
    except EmptyPage:
        filmsPage = paginator.page(paginator.num_pages)

    nombre_film = Films.objects.all().count()
    form_view_film = FilmForm(request.POST or None, request.FILES)
    if request.method == "POST":
        if form_view_film.is_valid():
            # form_view_film.save()
            currentuser = request.user
            titre = form_view_film.cleaned_data['titre']
            acteur = form_view_film.cleaned_data['acteur']
            description = form_view_film.cleaned_data['description']
            language = form_view_film.cleaned_data['language']
            resolution = form_view_film.cleaned_data['resolution']
            cover = form_view_film.cleaned_data['cover']
            film = form_view_film.cleaned_data['film']
            prix = form_view_film.cleaned_data['prix_telechargement']

            Films(user = currentuser,titre = titre,acteur = acteur,description = description,language = language,resolution = resolution,cover = cover,film = film,prix_telechargement = prix ).save()
            nombre_film = Films.objects.all().count()
            msg = "Enregistrer avec success !!!"

    return render(request, 'home.html', locals() )


def apropos_app(request):
    return render(request, 'about.html', locals() )

def details_app(request,slug):
    film_obj = Films.objects.get( slug = slug )
    comm_obj = Commentaires.objects.filter( titre = film_obj )
    all_likes = Avis.objects.filter(Q(likes=True)).count()
    all_dislikes = Avis.objects.filter(Q(dislikes=True)).count()

    form_view_comm = CommentaireForm(request.POST or None)
    if request.method == "POST":
        if form_view_comm.is_valid():
            current_user = request.user
            # titr = form_view_comm.cleaned_data['titre']
            com = form_view_comm.cleaned_data['commentaire']
            Commentaires(user = current_user,titre = film_obj,commentaire = com).save()
            msg = "Enregistrer avec success !!!"
            form_view_comm = Commentaires()

    form_view_avi = LikeForm(request.POST or None)
    current_user = request.user
    film_key = str(current_user)+str(slug)
    if request.method == "POST":
        if form_view_avi.is_valid():
            like = form_view_avi.cleaned_data['likes']
            dislike = form_view_avi.cleaned_data['dislikes']
            Avis( user = current_user, slug_key = film_key, likes = like, dislikes = dislike ).save()
            all_likes = Avis.objects.filter(Q(likes=True) & Q(slug_key=film_obj)).count()
            all_dislikes = Avis.objects.filter(Q(dislikes=True) & Q(slug_key=film_obj)).count()

    return render(request, 'detail.html', locals() )

def contact_app(request):
    return render(request, 'contact.html', locals() )

def ajout_app(request):
    form_view_film = FilmForm(request.POST or None, request.FILES)
    if request.method == "POST":
        if form_view_film.is_valid():
            # form_view_film.save()
            currentuser = request.user
            titre = form_view_film.cleaned_data['titre']
            acteur = form_view_film.cleaned_data['acteur']
            description = form_view_film.cleaned_data['description']
            language = form_view_film.cleaned_data['language']
            resolution = form_view_film.cleaned_data['resolution']
            cover = form_view_film.cleaned_data['cover']
            film = form_view_film.cleaned_data['film']
            prix = form_view_film.cleaned_data['prix_telechargement']

            Films(user = currentuser,titre = titre,acteur = acteur,description = description,language = language,resolution = resolution,cover = cover,film = film,prix_telechargement = prix ).save()
            nombre_film = Films.objects.all().count()
            msg = "Enregistrer avec success !!!"
    return render(request, 'ajouter_film.html', locals() )
