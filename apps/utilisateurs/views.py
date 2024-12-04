# preparateurs/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

def home(request):
    return render(request, 'base.html', {
        'titre': 'QuickLab',
    })

def accueil(request):
    return render(request, 'accueil.html', {
        'titre': '',
    })

def produits(request):
    produits = Produit.objects.all()
    return render(request, 'produits.html', {
        'titre': 'QuickLab',
        'produits': produits
    })

def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('accueil')
    else:
        form = UserCreationForm()
    return render(request, 'preparateurs/inscription.html', {'form': form})

class ConnexionView(LoginView):
    template_name = 'utilisateurs/connexion.html'

def liste_utilisateurs(request):
    User = get_user_model()
    utilisateurs = User.objects.all()
    return render(request, 'utilisateurs/liste_utilisateurs.html', {
        'utilisateurs': utilisateurs
    })

