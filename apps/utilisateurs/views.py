# preparateurs/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

def home(request):
    return render(request, 'base.html', {
        'titre': 'QuickLab',
    })

def accueil(request):

    if request.user.is_authenticated:
        return render(request, 'utilisateurs/accueil.html', {
            'titre': 'QuickLab',
        })
    else:
        return redirect('connexion')

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


def deconnexion(request):

    logout(request)
    return redirect('connexion')

class ConnexionView(LoginView):
    template_name = 'utilisateurs/connexion.html'
    success_url = 'accueil'
    redirect_authenticated_user = False

    def get_success_url(self):
        return self.success_url
