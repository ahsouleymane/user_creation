from django.shortcuts import redirect, render

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User

from user_creation import settings
from django.core.mail import send_mail, EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from profil.token import generatorToken


# Create your views here.

def home(request):
    return render(request, "profil/base.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        this_user = User.objects.get(username = username)

        if user is not None:
            auth_login(request, user)
            prenom = user.first_name
            return render(request, "profil/manage_partners_health.html", {'prenom': prenom})
        elif this_user.is_active == False:
            messages.error(request, 'S\'il vous plait veuillez activer votre compte avant de vous connectez !!!')
        else:
            messages.error(request, 'Nom utilisateur ou mot de passe incorrect !!!')
            return redirect('login')

    return render(request, "profil/login.html")

def logout(request):
    return render(request, 'profil/login.html')

def register(request):
    if request.method == 'POST':
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        profession = request.POST['profession']
        genre = request.POST['genre']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if User.objects.filter(username = username):
            messages.error(request, 'Cet nom d\'utilisateur existe déja !!!')
            return redirect('register')

        elif User.objects.filter(email = email):
            messages.error(request, 'Cet Email a déja un compte !!!')
            return redirect('register')

        elif password != password1:
            messages.error(request, 'Echec de confirmation du mot de passe !!!')
            return redirect('register')

        elif not username.isalnum():
            messages.error(request, 'Le nom d\'utilisateur n\'est pas alphanumerique !!!')
            return redirect('register')

        mon_util = User.objects.create_user(username, email, password)
        mon_util.first_name = nom
        mon_util.last_name = prenom
        mon_util.profession = profession
        mon_util.genre = genre
        mon_util.save()

    return render(request, "profil/register.html")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Félicitation !!!  votre compte a été crée avec succès !!!")
        return redirect('login')
    else:
        messages.error(request, "Erreur lors de la céation de votre compte, Réessayer !!!")
        return redirect('register')