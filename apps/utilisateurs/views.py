# preparateurs/views.py
import json
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
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
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
        'utilisateurs': utilisateurs,  # Les utilisateurs sont transmis au template
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
                password=utilisateur["prenom"],
                prenom=utilisateur["prenom"],
                nom=utilisateur["nom"],
                email=utilisateur["email"],
                groupe=utilisateur["groupe"],
                annee=annee,
                role="etudiant"
            )

        del request.session["utilisateurs_preview"]

        return redirect("utilisateurs:liste_utilisateurs")

    return render(request, "utilisateurs/preparateurs/importer_utilisateurs.html", {
        "utilisateurs_preview": utilisateurs_preview
    })
    
from django.http import JsonResponse

@login_required
def supprimer_utilisateurs(request):
    if request.method == "POST":
        utilisateurs_ids = request.POST.getlist('utilisateurs')
        utilisateur_connecte = request.user

        # Filtrer les utilisateurs sélectionnés
        utilisateurs_a_supprimer = Utilisateur.objects.filter(id__in=utilisateurs_ids)
        utilisateurs_autorises = []

        for utilisateur in utilisateurs_a_supprimer:
            # Règles pour les préparateurs
            if utilisateur_connecte.role == "preparateur":
                if utilisateur.role == "etudiant":  # Préparateurs peuvent supprimer uniquement les étudiants
                    utilisateurs_autorises.append(utilisateur)

            # Règles pour les administrateurs
            elif utilisateur_connecte.role == "administrateur":
                if utilisateur.role in ["etudiant", "preparateur"]:  # Administrateurs peuvent supprimer étudiants et préparateurs
                    utilisateurs_autorises.append(utilisateur)

        # Suppression des utilisateurs autorisés
        if utilisateurs_autorises:
            count = len(utilisateurs_autorises)
            Utilisateur.objects.filter(id__in=[u.id for u in utilisateurs_autorises]).delete()

            # Réponse JSON pour les requêtes AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    "success": True,
                    "count": count,
                    "message": f"{count} utilisateur(s) supprimé(s) avec succès."
                })

            # Message classique pour les requêtes non AJAX
            messages.success(request, f"{count} utilisateur(s) supprimé(s) avec succès.")
        else:
            error_message = "Vous n'êtes pas autorisé à supprimer les utilisateurs sélectionnés."

            # Réponse JSON pour les requêtes AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    "success": False,
                    "message": error_message
                })

            # Message classique pour les requêtes non AJAX
            messages.error(request, error_message)

        return redirect('utilisateurs:liste_utilisateurs')

    return JsonResponse({"error": "Requête invalide."}, status=400)

@login_required
def modifier_utilisateur(request, utilisateur_id):
    utilisateur_connecte = request.user

    # Récupérer l'utilisateur ou renvoyer une erreur 404
    utilisateur = get_object_or_404(Utilisateur, id=utilisateur_id)

    # Vérifier les autorisations
    if utilisateur_connecte.role == "preparateur" and utilisateur.role != "etudiant":
        return JsonResponse({"success": False, "message": "Vous n’êtes pas autorisé à modifier cet utilisateur."}, status=403)
    elif utilisateur_connecte.role == "administrateur" and utilisateur.role == "administrateur" and utilisateur != utilisateur_connecte:
        return JsonResponse({"success": False, "message": "Vous ne pouvez pas modifier un autre administrateur."}, status=403)

    # Si c'est une requête GET, envoyer les données utilisateur
    if request.method == "GET":
        return JsonResponse({
            "success": True,
            "nom": utilisateur.nom,
            "prenom": utilisateur.prenom,
            "email": utilisateur.email,
            "annee": utilisateur.annee,
            "groupe": utilisateur.groupe,
        })

    # Si c'est une requête POST, mettre à jour l'utilisateur
    if request.method == "POST":
        data = json.loads(request.body)
        utilisateur.nom = data.get('nom')
        utilisateur.prenom = data.get('prenom')
        utilisateur.email = data.get('email')
        utilisateur.annee = data.get('annee')
        utilisateur.groupe = data.get('groupe')
        utilisateur.save()

        return JsonResponse({"success": True, "message": "Utilisateur modifié avec succès."})

    return JsonResponse({"success": False, "message": "Requête invalide."}, status=400)