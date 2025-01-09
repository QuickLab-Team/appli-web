# preparateurs/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from .forms import UtilisateurForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
import openpyxl
from django.shortcuts import render, redirect
from .models import Utilisateur

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
    query = request.GET.get('q', '')  # Recherche
    role = request.GET.get('role', '')  # Filtre par rôle
    annee = request.GET.get('annee', '')  # Filtre par année
    groupe = request.GET.get('groupe', '')  # Filtre par groupe

    # Filtrer les utilisateurs selon les critères
    utilisateurs = User.objects.all()
    if query:
        utilisateurs = utilisateurs.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(email__icontains=query)
        )
    if role:
        utilisateurs = utilisateurs.filter(role=role)
    if annee:
        utilisateurs = utilisateurs.filter(annee=annee)
    if groupe:
        utilisateurs = utilisateurs.filter(groupe=groupe)

    # Vérifier si la requête est en AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('utilisateurs/includes/utilisateurs_table.html', {'utilisateurs': utilisateurs})
        return JsonResponse({'html': html})

    return render(request, 'utilisateurs/preparateurs/liste_utilisateurs.html', {
        'utilisateurs': utilisateurs,
        'roles': User.ROLES,
        'annees': User.ANNEES,
        'groupes': User.GROUPS,
        'query': query,
        'selected_role': role,
        'selected_annee': annee,
        'selected_groupe': groupe,
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

def importer_utilisateurs(request):
    utilisateurs_preview = []

    if request.method == "POST" and "fichier" in request.FILES:
        fichier = request.FILES["fichier"]
        workbook = openpyxl.load_workbook(fichier)
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not row[1] or not row[2] or not row[6] or not row[4]:
                break
            groupe = row[4]
            if isinstance(groupe, (int, float)):
                groupe = f"Groupe {int(groupe)}"
            elif isinstance(groupe, str) and groupe.isdigit():
                groupe = f"Groupe {groupe}"
            
            utilisateurs_preview.append({
                "nom": row[1],        # Colonne B (Nom)
                "prenom": row[2],     # Colonne C (Prénom)
                "email": row[6],      # Colonne G (Email)
                "groupe": groupe,     # Groupe
            })

        request.session["utilisateurs_preview"] = utilisateurs_preview

    elif request.method == "POST" and "importer" in request.POST:
        annee = request.POST.get("annee")
        utilisateurs_preview = request.session.get("utilisateurs_preview", [])

        for utilisateur in utilisateurs_preview:
            Utilisateur.objects.create(
                prenom=utilisateur["prenom"],
                nom=utilisateur["nom"],
                email=utilisateur["email"],
                groupe=utilisateur["groupe"],
                annee=annee,
            )

        del request.session["utilisateurs_preview"]

        return redirect("utilisateurs:liste_utilisateurs")

    return render(request, "utilisateurs/preparateurs/importer_utilisateurs.html", {
        "utilisateurs_preview": utilisateurs_preview
    })