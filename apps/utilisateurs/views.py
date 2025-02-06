# preparateurs/views.py
import json
import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.utils.translation import gettext_lazy as _

from quicklab import settings
from .forms import UtilisateurForm
from produits.models import Produit, Famille, Service
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import BadHeaderError, JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
import openpyxl
from django.shortcuts import render, redirect
from .models import Utilisateur
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now, timedelta
from django.shortcuts import render
from reservations.models import Reservation
from django.db.models import Count

def home(request):
    return render(request, 'base.html', {
        'titre': 'QuickLab',
    })

def test(request):
    return render(request, 'utilisateurs/etudiants/accueil.html', {
        'titre': 'QuickLab',
    })


@login_required
def accueil(request):

    if request.user.role == 'etudiant':
            return render(request, 'utilisateurs/etudiants/accueil.html', {
                'titre': 'QuickLab',
                'produits': Produit.objects.all(),
                'familles': Famille.objects.all().distinct(),
                'services': Service.objects.all().order_by('nom')
            })
        
    elif request.user.role == 'preparateur' or request.user.role == 'administrateur': 
            return render(request, 'utilisateurs/preparateurs/accueil.html', {
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

    # Calculer le nombre d'étudiants
    student_count = utilisateurs.filter(role='etudiant').count()

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
        'student_count': student_count,
        'titre': 'QuickLab',
    })


@login_required
def ajouter_utilisateur(request):
    if request.method == 'POST':
        form = UtilisateurForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('utilisateurs:liste_utilisateurs')
    else:
        form = UtilisateurForm(user=request.user)

    return render(request, 'utilisateurs/preparateurs/ajouter_utilisateur.html', {'form': form, 'titre': 'QuickLab'})


def importer_utilisateurs(request):
    utilisateurs_preview = []

    if request.method == "POST" and "fichier" in request.FILES:
        fichier = request.FILES["fichier"]
        workbook = openpyxl.load_workbook(fichier)
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not row[1] or not row[2] or not row[6] or not row[4]:
                continue  # Ignore les lignes incomplètes
            
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
        erreurs = []

        for utilisateur in utilisateurs_preview:
            email = utilisateur["email"]
            
            # Vérifie si l'utilisateur existe déjà
            if Utilisateur.objects.filter(email=email).exists():
                erreurs.append(f"L'utilisateur avec l'email {email} existe déjà.")
                continue

            # Générer un mot de passe provisoire
            mot_de_passe = get_random_string(length=6, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*')
            
            # Créer un nouvel utilisateur
            user = Utilisateur.objects.create(
                prenom=utilisateur["prenom"],
                nom=utilisateur["nom"],
                email=email,
                groupe=utilisateur["groupe"],
                annee=annee,
                role="etudiant"
            )
            user.set_password(mot_de_passe)
            user.save()

            # Envoyer un email de bienvenue avec le mot de passe provisoire
            message = f"""
            Bonjour {user.prenom},

            Bienvenue sur QuickLab ! Voici vos identifiants de connexion :

            Email : {user.email}
            Mot de passe provisoire : {mot_de_passe}

            Veuillez vous connecter et changer votre mot de passe dès que possible.

            Cordialement,
            L'équipe QuickLab
            """

            if os.environ.get('ENV') == 'prod':
                mail = user.email
            elif os.environ.get('EMAIL_DEV'):
                mail = os.environ.get('EMAIL_DEV')
            else:
                mail = settings.EMAIL_HOST_USER
                
            send_mail(
                subject="Bienvenue sur QuickLab",
                message=message,
                from_email='QuickLab <votre_email@gmail.com>',
                recipient_list=[mail],
                fail_silently=False,
            )

        # Supprimer les données de prévisualisation après l'import
        del request.session["utilisateurs_preview"]

        if erreurs:
            messages.warning(request, "Certains utilisateurs n'ont pas été importés : " + ", ".join(erreurs))
        else:
            messages.success(request, "Tous les utilisateurs ont été importés avec succès.")

        return redirect("utilisateurs:liste_utilisateurs")

    return render(request, "utilisateurs/preparateurs/importer_utilisateurs.html", {
        "utilisateurs_preview": utilisateurs_preview,
        'titre': 'QuickLab',
    })

@login_required
def supprimer_utilisateurs(request):
    if request.method == "POST":
        data = json.loads(request.body)  # Pour récupérer les données JSON
        utilisateurs_ids = data.get("utilisateurs", [])  # Récupérer les IDs envoyés
        utilisateur_connecte = request.user

        # Règles pour filtrer les utilisateurs
        utilisateurs_a_supprimer = Utilisateur.objects.filter(id__in=utilisateurs_ids)
        utilisateurs_autorises = []

        for utilisateur in utilisateurs_a_supprimer:
            if utilisateur_connecte.role == "preparateur" and utilisateur.role == "etudiant":
                utilisateurs_autorises.append(utilisateur)
            elif utilisateur_connecte.role == "administrateur" and utilisateur.role in ["etudiant", "preparateur"]:
                utilisateurs_autorises.append(utilisateur)

        if utilisateurs_autorises:
            count = len(utilisateurs_autorises)
            Utilisateur.objects.filter(id__in=[u.id for u in utilisateurs_autorises]).delete()

            return JsonResponse({"success": True, "message": f"{count} utilisateur(s) supprimé(s) avec succès."})

        return JsonResponse({"success": False, "message": "Vous n'êtes pas autorisé à supprimer ces utilisateurs."})

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

@login_required
def mon_compte(request):
    """Vue pour afficher les informations de compte."""
    if request.user.role == 'etudiant':
        return render(request, 'utilisateurs/etudiants/compte.html')
    
    return render(request, 'utilisateurs/preparateurs/mon_compte.html', {
        'user': request.user
    })

class PasswordChangeFormFrancais(PasswordChangeForm):
    """Formulaire personnalisé pour afficher les erreurs en français."""
    error_messages = {
        'password_incorrect': _("L'ancien mot de passe est incorrect."),
        'password_mismatch': _("Les deux mots de passe ne correspondent pas."),
        'password_too_short': _("Votre mot de passe doit contenir au moins 8 caractères."),
        'password_too_common': _("Votre mot de passe est trop courant."),
        'password_entirely_numeric': _("Votre mot de passe ne peut pas être uniquement composé de chiffres."),
        'password_similar': _("Votre mot de passe est trop similaire à vos informations personnelles."),
    }

@login_required
def changer_mot_de_passe(request):
    """Vue pour permettre à l'utilisateur de changer son mot de passe."""
    if request.method == 'POST':
        form = PasswordChangeFormFrancais(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Votre mot de passe a été changé avec succès.')
            return redirect('utilisateurs:mon_compte')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = PasswordChangeFormFrancais(user=request.user)

    template_name = 'utilisateurs/etudiants/changer_mot_de_passe.html' if request.user.role == 'etudiant' else 'utilisateurs/preparateurs/changer_mot_de_passe.html'
    
    return render(request, template_name, {'form': form})

@login_required
def statistiques(request):
    aujourd_hui = now().date()
    debut_mois = aujourd_hui.replace(day=1)

    # Définir les années possibles
    annees_possibles = ["1ère année", "2ème année", "3ème année"]

    # Initialiser les dictionnaires avec toutes les années à 0
    etudiants_connectes_aujourdhui = {annee: 0 for annee in annees_possibles}
    etudiants_connectes_mois = {annee: 0 for annee in annees_possibles}
    reservations_etudiants_aujourdhui = {annee: 0 for annee in annees_possibles}
    reservations_etudiants_mois = {annee: 0 for annee in annees_possibles}

    # Connexions des étudiants
    for res in Utilisateur.objects.filter(role='etudiant', last_login__date=aujourd_hui).values('annee').annotate(total=Count('id')):
        etudiants_connectes_aujourdhui[res['annee']] = res['total']

    for res in Utilisateur.objects.filter(role='etudiant', last_login__date__gte=debut_mois).values('annee').annotate(total=Count('id')):
        etudiants_connectes_mois[res['annee']] = res['total']

    # Réservations des étudiants
    for res in Reservation.objects.filter(utilisateur__role='etudiant', date__date=aujourd_hui).values('utilisateur__annee').annotate(total=Count('id')):
        reservations_etudiants_aujourdhui[res['utilisateur__annee']] = res['total']

    for res in Reservation.objects.filter(utilisateur__role='etudiant', date__date__gte=debut_mois).values('utilisateur__annee').annotate(total=Count('id')):
        reservations_etudiants_mois[res['utilisateur__annee']] = res['total']

    # Convertir en JSON
    data_statistiques = json.dumps({
        "etudiants_connectes_aujourdhui": etudiants_connectes_aujourdhui,
        "etudiants_connectes_mois": etudiants_connectes_mois,
        "reservations_etudiants_aujourdhui": reservations_etudiants_aujourdhui,
        "reservations_etudiants_mois": reservations_etudiants_mois,
    })

    return render(request, 'utilisateurs/preparateurs/statistiques.html', {'data_statistiques': data_statistiques})