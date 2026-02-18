from django.shortcuts import render, get_object_or_404
from .models import Offre

# Page d'accueil
def home(request):
    # On récupère les 6 dernières offres disponibles
    offres = Offre.objects.filter(statut='disponible').order_by('-id')[:6]
    return render(request, "home.html", {"offres": offres})

# Liste de toutes les offres
def offres_list(request):
    offres = Offre.objects.filter(statut='disponible').order_by('-id')
    return render(request, "offres/liste_offres.html", {"offres": offres})

# Détail d'une offre
def offre_detail(request, id):
    offre = get_object_or_404(Offre, id=id)
    return render(request, "offres/details_offre.html", {"offre": offre})
