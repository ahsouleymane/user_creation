from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

class creerUtillisateur(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'lastname', 'profession', 'genre']
        labels = {
            'username': 'Nom utilisateur',
            'email': 'Email',
            'password1': 'Mot de passe',
            'password2': 'Confirmer le mot de passe',
            'first_name': 'Nom',
            'last_name': 'Prénom',
            'profession': 'Profession',
            'genre': 'Genre',
        }
