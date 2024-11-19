# preparateurs/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

def accueil(request):
    return render(request, 'preparateurs/accueil.html')

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
    template_name = 'preparateurs/connexion.html'
