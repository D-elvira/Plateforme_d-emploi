from django.shortcuts import render, get_object_or_404, redirect
from .models import Offre
from django.db.models import Q
from .forms import CandidatureForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Candidature

# Page d'accueil intelligente
def home(request):
    # Par défaut, on prend les 6 dernières offres disponibles
    offres = Offre.objects.filter(statut='disponible').order_by('-id')

    # Si l'utilisateur est connecté et a choisi des domaines (DA)
    if request.user.is_authenticated and hasattr(request.user, 'domaine_activite') and request.user.domaine_activite:
        # On transforme sa chaîne "Domaine1,Domaine2" en liste ['Domaine1', 'Domaine2']
        domaines_utilisateur = request.user.domaine_activite.split(',')

        # On filtre : l'offre doit avoir un domaine présent dans la liste de l'utilisateur
        # On utilise __in pour comparer le champ domaine de l'offre à la liste
        offres_personnalisees = offres.filter(categorie__in=domaines_utilisateur)[:6]

        # Si on trouve des offres correspondantes, on les affiche
        if offres_personnalisees.exists():
            return render(request, "home.html", {"offres": offres_personnalisees, "personnalise": True})

    # Si non connecté ou pas d'offres dans ses DA, on montre les 6 dernières
    return render(request, "home.html", {"offres": offres[:6], "personnalise": False})


# Liste de toutes les offres
def offres_list(request):
    offres = Offre.objects.filter(statut='disponible').order_by('-id')
    return render(request, "offres/list_offres.html", {"offres": offres})


def offre_detail(request, id):  # Garde 'id' ou 'pk' selon ton url
    offre = get_object_or_404(Offre, id=id)

    if request.method == 'POST':
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.offre = offre
            candidature.save()
            messages.success(request, "Votre candidature a été envoyée avec succès !")
            return redirect('offre_detail', id=offre.id)
    else:
        form = CandidatureForm()

    return render(request, 'offres/offre_detail.html', {'offre': offre, 'form': form})

@login_required
def mes_candidatures(request):
    # On récupère les candidatures filtrées par l'email de l'utilisateur connecté
    # Ou mieux, si tu as lié Candidature à User : candidature.user = request.user
    candidatures = Candidature.objects.all().order_by('-date_envoi')
    return render(request, 'offres/mes_candidatures.html', {'candidatures': candidatures})