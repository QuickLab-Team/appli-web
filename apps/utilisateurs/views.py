# preparateurs/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from .forms import UtilisateurForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'base.html', {
        'titre': 'QuickLab',
    })

@login_required
def accueil(request):

    if request.user.role == 'etudiant':
            return render(request, 'produits/etudiants/produits.html', {
                'titre': 'QuickLab',
            })
        
    elif request.user.role == 'preparateur' or request.user.role == 'administrateur': 
            return render(request, 'utilisateurs/accueil.html', {
                'titre': 'QuickLab',
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


def deconnexion(request):

    logout(request)
    return redirect('utilisateurs:connexion')

class ConnexionView(LoginView):
    template_name = 'utilisateurs/connexion.html'
    success_url = 'accueil'
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.success_url

def liste_utilisateurs(request):
    User = get_user_model()
    utilisateurs = User.objects.all()
    return render(request, 'utilisateurs/preparateurs/liste_utilisateurs.html', {
        'utilisateurs': utilisateurs
    })


def ajouter_utilisateur(request):
    if request.method == 'POST':
        form = UtilisateurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('utilisateurs:liste_utilisateurs')
    else:
        form = UtilisateurForm()
    return render(request, 'utilisateurs/preparateurs/ajouter_utilisateur.html', {'form': form})

def importer_utilisateurs(request):
    return render(request, 'utilisateurs/preparateurs/importer_utilisateurs.html', {
        'titre': 'QuickLab',
    })