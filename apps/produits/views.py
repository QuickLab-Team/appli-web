from django.shortcuts import render, redirect
from .models import Produit, Famille, Stockage, Fournisseur, Service
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pandas as pd
from paniers.models import Panier
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import csv

@login_required
def exporter_produits(request):
    if request.user.role not in ['preparateur', 'administrateur']:
        return HttpResponse(status=403)

    produits = Produit.objects.all().order_by('nom')
    
    # Récupération des filtres depuis les paramètres GET
    query = request.GET.get('q', '')
    selected_famille = request.GET.get('famille', '')
    selected_fournisseur = request.GET.get('fournisseur', '')
    selected_stockage = request.GET.get('stockage', '')
    selected_service = request.GET.get('service', '')

    # Application des filtres dynamiques
    if query:
        produits = produits.filter(nom__icontains=query)
    if selected_famille:
        produits = produits.filter(familles__id=selected_famille)
    if selected_fournisseur:
        produits = produits.filter(fournisseur__id=selected_fournisseur)
    if selected_stockage:
        produits = produits.filter(stockage__id=selected_stockage)
    if selected_service:
        produits = produits.filter(stockage__service__id=selected_service)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="produits.csv"'

    writer = csv.writer(response)
    
    writer.writerow(["Nom", "Quantité", "Fournisseur", "Familles", "Date d'ajout", "Stockage", "Seuil", "Type"])

    for produit in produits:
        writer.writerow([
            produit.nom,
            produit.quantite,
            produit.fournisseur.nom if produit.fournisseur else "",
            ", ".join(f.nom for f in produit.familles.all()),
            produit.date_ajout.strftime("%Y-%m-%d %H:%M:%S"),
            produit.stockage.nom,
            produit.seuil,
            produit.get_type_display(),
        ])

    messages.success(request, "Produits exportés avec succès.")
    return response

@login_required
def produits(request):
    produits = Produit.objects.all().order_by('nom')
    familles = Famille.objects.all().order_by('nom')
    stockages = Stockage.objects.all().order_by('nom')
    fournisseurs = Fournisseur.objects.all().order_by('nom')

    # Récupération des filtres depuis les paramètres GET
    query = request.GET.get('q', '')
    selected_famille = request.GET.get('famille', '')
    selected_fournisseur = request.GET.get('fournisseur', '')
    selected_stockage = request.GET.get('stockage', '')
    selected_service = request.GET.get('service', '')

    # Application des filtres dynamiques
    if query:
        produits = produits.filter(nom__icontains=query)
    if selected_famille:
        produits = produits.filter(familles__id=selected_famille)
    if selected_fournisseur:
        produits = produits.filter(fournisseur__id=selected_fournisseur)
    if selected_stockage:
        produits = produits.filter(stockage__id=selected_stockage)
    if selected_service:
        produits = produits.filter(stockage__service__id=selected_service)

    # Gestion des rôles et rendu HTML
    if request.user.role in ['preparateur', 'administrateur']:
        return render(request, 'produits/preparateurs/produits.html', {
            'titre': 'QuickLab',
            'produits': produits,
            'familles': familles,
            'fournisseurs': fournisseurs,
            'stockages': stockages,
            'query': query,
            'selected_famille': selected_famille,
            'selected_fournisseur': selected_fournisseur,
            'selected_stockage': selected_stockage,
        })
    else:
        return render(request, 'produits/etudiants/produits.html', {
            'titre': 'QuickLab',
            'produits': produits,
            'familles': familles,
            'services': Service.objects.all().distinct(),
        })

@login_required
def importer_produits(request):
    services = Service.objects.all().distinct()

    if request.user.role not in ['preparateur', 'administrateur']:
        return HttpResponse(status=403)
    
    produits_preview = []

    if request.method == "POST" and "fichier" in request.FILES:
        fichier = request.FILES["fichier"]
        df = pd.read_excel(fichier, skiprows=3)

        for _, row in df.iterrows():
            quantite = 0.0
            if row["Quantité"]:
                quantite_str = str(row["Quantité"])
                quantite = ''.join(filter(str.isdigit, quantite_str))
                unite = ''.join(filter(str.isalpha, quantite_str)).lower()
                quantite = float(quantite) if quantite else 0

            famille = row.get("Fonction")
            fournisseur = row.get("Fournisseur")

            famille = famille if pd.notna(famille) and famille != "-" else "Pas de famille"
            fournisseur = fournisseur if pd.notna(fournisseur) and fournisseur != "-" else "Pas de fournisseur"
            produits_preview.append({
                "nom": row["Produits"],
                "fournisseur": fournisseur,
                "quantite": quantite,
                "unite": unite,
                "famille": famille,
                "stockage": row["Lieu de stockage"],
            })

        request.session["produits_preview"] = produits_preview

    elif request.method == "POST" and "importer" in request.POST:
        produits_preview = request.session.get("produits_preview", [])
        selected_service = request.POST.get("service")

        for produit in produits_preview:
            p = Produit.objects.create(
                nom=produit["nom"],
                quantite=0,
                stockage=Stockage.objects.get_or_create(nom=produit["stockage"], service=Service.objects.get(nom=selected_service))[0],
            )

            if produit["famille"] != "Pas de famille":
                p.add_famille(produit["famille"])

            if produit["fournisseur"] != "Pas de fournisseur":
                p.add_fournisseur(produit["fournisseur"])

            if produit["quantite"] and produit["unite"]:
                p.add_type(produit["unite"])
                if produit["unite"] == "ml":
                    p.quantite = produit["quantite"] / 1000
                elif produit["unite"] == "cl":
                    p.quantite = produit["quantite"] / 100
                elif produit["unite"] == "l":
                    p.quantite = produit["quantite"]
                elif produit["unite"] == "g":
                    p.quantite = produit["quantite"] / 1000
                elif produit["unite"] == "kg":
                    p.quantite = produit["quantite"]
                else:
                    p.quantite = produit["quantite"]

                p.save()

        del request.session["produits_preview"]
        return produits(request)
    
    elif request.method == "POST":
        return HttpResponse(status=400)

    return render(request, "produits/preparateurs/importer_produits.html", {
        "produits_preview": produits_preview,
        "services": services,
    })

@login_required
def produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.user.role in ['preparateur', 'administrateur']:
        return render(request, 'produits/preparateurs/produit.html', {
            'titre': 'QuickLab',
            'produit': produit,
        })
    else:
        panier = Panier.objects.get_or_create(utilisateur=request.user)[0]
        return render(request, 'produits/etudiants/produit.html', {
            'titre': 'QuickLab',
            'produit': produit,
            'in_panier': panier.produits.filter(produit=produit).exists(),
            'familles': Famille.objects.all().distinct(),
        })

@login_required
def ajouter_produit(request):
    if request.user.role not in ['preparateur', 'administrateur']:
        return HttpResponse(status=403)
    
    fournisseurs = Fournisseur.objects.all().order_by('nom')
    familles = Famille.objects.all().order_by('nom')
    stockages = Stockage.objects.all().order_by('nom')
    services = Service.objects.all().order_by('nom')

    if request.method == 'POST':
        nom = request.POST.get('nom')
        quantite = int(request.POST.get('quantite'))
        stockage = request.POST.get('stockage')
        unite = request.POST.get('unite')
        famille = request.POST.get('familles')
        fournisseur = request.POST.get('fournisseur')
        service = request.POST.get('service')

        if unite == "ml":
            type = 'liquide'
            quantite = quantite / 1000
        elif unite == "cl":
            type = 'liquide'
            quantite = quantite / 100
        elif unite == "l":
            type = 'liquide'
            quantite = quantite
        elif unite == "g":
            type = 'solide'
            quantite = quantite / 1000
        elif unite == "kg":
            type = 'solide'
            quantite = quantite
        else:
            type = 'unite'
            quantite = quantite

        p = Produit.objects.create(
            nom=nom,
            quantite=quantite,
            type=type,
            stockage=Stockage.objects.get_or_create(nom=stockage, service=Service.objects.get(nom=service))[0],
        )

        if fournisseur:
            p.add_fournisseur(fournisseur)
        
        
        p.add_famille(famille)
        p.save()


        return redirect('produits:produits')
   
    return render(request, "produits/preparateurs/ajouter_produit.html", {
        'fournisseurs': fournisseurs,
        'familles': familles,
        'services' : services,
        'stockages': stockages,
    })

@login_required
def modifier_produit(request, produit_id):
    if request.user.role not in ['preparateur', 'administrateur']:
        return HttpResponse(status=403)
    
    produit = get_object_or_404(Produit, id=produit_id)
    fournisseurs = Fournisseur.objects.all().order_by('nom')
    familles = Famille.objects.all().order_by('nom')
    services = Service.objects.all().order_by('nom')
    stockages = Stockage.objects.all().order_by('nom')

    if request.method == 'POST':
        produit.nom = request.POST.get('nom')
        quantite = request.POST.get('quantite')
        unite = request.POST.get('unite')
        
        produit.fournisseur = Fournisseur.objects.get_or_create(nom=request.POST.get('fournisseur'))[0]

        famille = request.POST.get('familles')
        fournisseur = request.POST.get('fournisseur')

        service_nom = request.POST.get('service')
        service, created = Service.objects.get_or_create(nom=service_nom)
        produit.familles.clear()
        produit.stockage = Stockage.objects.get_or_create(nom=request.POST.get('stockage'), service=service)[0]
        produit.add_famille(famille)

        if fournisseur:
            produit.add_fournisseur(fournisseur)

        produit.save()
        return redirect('produits:produit', produit_id=produit.id)

    return render(request, "produits/preparateurs/modifier_produit.html", {
        'produit': produit,
        'fournisseurs': fournisseurs,
        'familles': familles,
        'services': services,
        'stockages': stockages,
    })

@login_required
def supprimer_produit(request, produit_id):
    if request.user.role not in ['preparateur', 'administrateur']:
        return HttpResponse(status=403)
    
    if request.method == 'POST':
        produit = get_object_or_404(Produit, id=produit_id)
        produit.delete()
        messages.success(request, "Produit supprimé avec succès.")
        return redirect('produits:produits')
    
    return HttpResponse(status=405)

@csrf_exempt
def add_service(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        service_name = data.get('name')
        if service_name:
            service, created = Service.objects.get_or_create(nom=service_name)
            if created:
                return JsonResponse({'success': True, 'service': service_name})
            else:
                return JsonResponse({'success': False, 'error': 'Service already exists'})
        return JsonResponse({'success': False, 'error': 'Invalid data'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def fournisseurs(request):
    query = request.GET.get('q', '')
    fournisseurs = Fournisseur.objects.all().order_by("nom")
    if query:
        fournisseurs = fournisseurs.filter(nom__icontains=query)
    return render(request, "produits/preparateurs/fournisseurs.html", {
        'fournisseurs': fournisseurs,
        'query': query,
    })

@login_required
def ajouter_fournisseur(request):
    if request.user.role not in ['preparateur', 'administrateur']:
        return HttpResponse(status=403)
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        Fournisseur.objects.create(nom=nom)
        return redirect('produits:fournisseurs')
    
    return render(request, "produits/preparateurs/ajouter_fournisseur.html")

@login_required
def stockages(request):
    query = request.GET.get('q', '')
    selected_service = request.GET.get('service', '')
    stockages = Stockage.objects.all().order_by("nom")
    services = Service.objects.all().distinct()

    if query:
        stockages = stockages.filter(nom__icontains=query)
    if selected_service:
        stockages = stockages.filter(service__id=selected_service)

    return render(request, "produits/preparateurs/stockages.html", {
        'stockages': stockages,
        'services': services,
        'query': query,
        'selected_service': selected_service,
    })

@login_required
def ajouter_stockage(request):
    if request.user.role not in ['preparateur', 'administrateur']:
        return HttpResponse(status=403)

    services = Service.objects.all().order_by('nom')

    if request.method == 'POST':
        nom = request.POST.get('nom')
        service_id = request.POST.get('service')
        service = get_object_or_404(Service, id=service_id)
        Stockage.objects.create(nom=nom, service=service)
        return redirect('produits:stockages')

    return render(request, "produits/preparateurs/ajouter_stockage.html", {
        'services': services,
    })

@login_required
def modifier_stockage(request, stockage_id):
    if request.user.role not in ['preparateur', 'administrateur']:
        return HttpResponse(status=403)

    stockage = get_object_or_404(Stockage, id=stockage_id)
    services = Service.objects.all().order_by('nom')

    if request.method == 'POST':
        stockage.nom = request.POST.get('nom')
        service_id = request.POST.get('service')
        stockage.service = get_object_or_404(Service, id=service_id)
        stockage.save()
        return redirect('produits:stockages')

    return render(request, "produits/preparateurs/modifier_stockage.html", {
        'stockage': stockage,
        'services': services,
    })

@login_required
def supprimer_stockage(request, stockage_id):
    if request.user.role not in ['preparateur', 'administrateur']:
        return HttpResponse(status=403)

    if request.method == 'POST':
        stockage = get_object_or_404(Stockage, id=stockage_id)
        stockage.delete()
        messages.success(request, "Stockage supprimé avec succès.")
        return redirect('produits:stockages')

    return HttpResponse(status=405)

@login_required
def modifier_fournisseur(request, fournisseur_id):
    if request.user.role not in ['preparateur', 'administrateur']:
        return HttpResponse(status=403)

    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)

    if request.method == 'POST':
        fournisseur.nom = request.POST.get('nom')
        fournisseur.save()
        return redirect('produits:fournisseurs')

    return render(request, "produits/preparateurs/modifier_fournisseur.html", {
        'fournisseur': fournisseur,
    })

@login_required
def supprimer_fournisseur(request, fournisseur_id):
    if request.user.role not in ['preparateur', 'administrateur']:
        return HttpResponse(status=403)

    if request.method == 'POST':
        fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
        fournisseur.delete()
        messages.success(request, "Fournisseur supprimé avec succès.")
        return redirect('produits:fournisseurs')

    return HttpResponse(status=405)


@login_required
def fournisseur_detail(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    produits = Produit.objects.filter(fournisseur=fournisseur).order_by('nom')

    return render(request, "produits/preparateurs/fournisseur_detail.html", {
        'fournisseur': fournisseur,
        'produits': produits,
    })

@login_required
def stockage_detail(request, stockage_id):
    stockage = get_object_or_404(Stockage, id=stockage_id)
    produits = Produit.objects.filter(stockage=stockage).order_by('nom')

    return render(request, "produits/preparateurs/stockage_detail.html", {
        'stockage': stockage,
        'produits': produits,
    })

