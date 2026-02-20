from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from offres.models import Offre, Entreprise, Candidature
from .recruteur_forms import OffreForm


def recruteur_required(view_func):
    """Décorateur pour vérifier que l'utilisateur est un recruteur."""

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if request.user.role != "recruteur":
            return HttpResponseForbidden("Accès réservé aux recruteurs.")
        return view_func(request, *args, **kwargs)

    return wrapper


def get_entreprise(user):
    """Récupère ou crée l'entreprise associée au recruteur."""
    try:
        return Entreprise.objects.get(user=user)
    except Entreprise.DoesNotExist:
        return Entreprise.objects.create(
            user=user,
            nom=user.company_name or user.username,
            ville=user.company_city or "",
            domaine=user.company_domain or "",
        )


@recruteur_required
def recruteur_dashboard(request):
    """Dashboard principal du recruteur."""
    entreprise = get_entreprise(request.user)
    mes_offres = Offre.objects.filter(entreprise=entreprise).order_by("-id")
    total_offres = mes_offres.count()
    offres_actives = mes_offres.filter(statut="disponible").count()
    total_candidatures = Candidature.objects.filter(
        offre__entreprise=entreprise
    ).count()

    # Dernières candidatures reçues
    dernieres_candidatures = (
        Candidature.objects.filter(offre__entreprise=entreprise)
        .select_related("offre")
        .order_by("-date_envoi")[:5]
    )

    # Top offres par nb de candidatures
    top_offres = []
    for offre in mes_offres[:5]:
        nb = offre.candidatures.count()
        top_offres.append({"offre": offre, "nb_candidatures": nb})

    context = {
        "active_page": "dashboard",
        "entreprise": entreprise,
        "total_offres": total_offres,
        "offres_actives": offres_actives,
        "total_candidatures": total_candidatures,
        "dernieres_candidatures": dernieres_candidatures,
        "top_offres": top_offres,
        "mes_offres": mes_offres[:5],
    }
    return render(request, "recruteur/recruteur_dashboard.html", context)


@recruteur_required
def recruteur_poster_offre(request):
    """Publier une nouvelle offre."""
    entreprise = get_entreprise(request.user)

    if request.method == "POST":
        form = OffreForm(request.POST)
        if form.is_valid():
            offre = form.save(commit=False)
            offre.entreprise = entreprise
            offre.save()
            messages.success(
                request, f"L'offre « {offre.titre} » a été publiée avec succès !"
            )
            return redirect("recruteur_mes_offres")
        else:
            messages.error(request, "Veuillez corriger les erreurs.")
    else:
        form = OffreForm()

    return render(
        request,
        "recruteur/recruteur_poster_offre.html",
        {
            "form": form,
            "active_page": "poster",
            "entreprise": entreprise,
        },
    )


@recruteur_required
def recruteur_mes_offres(request):
    """Liste de mes offres."""
    entreprise = get_entreprise(request.user)
    offres = Offre.objects.filter(entreprise=entreprise).order_by("-id")

    offres_data = []
    for offre in offres:
        nb = offre.candidatures.count()
        offres_data.append({"offre": offre, "nb_candidatures": nb})

    return render(
        request,
        "recruteur/recruteur_mes_offres.html",
        {
            "offres_data": offres_data,
            "active_page": "offres",
            "entreprise": entreprise,
        },
    )


@recruteur_required
def recruteur_candidatures(request, offre_id):
    """Voir les candidatures pour une offre précise."""
    entreprise = get_entreprise(request.user)
    offre = get_object_or_404(Offre, id=offre_id, entreprise=entreprise)
    candidatures = offre.candidatures.all().order_by("-date_envoi")

    return render(
        request,
        "recruteur/recruteur_candidatures.html",
        {
            "offre": offre,
            "candidatures": candidatures,
            "active_page": "offres",
            "entreprise": entreprise,
        },
    )


@recruteur_required
def recruteur_modifier_offre(request, offre_id):
    """Modifier une offre existante."""
    entreprise = get_entreprise(request.user)
    offre = get_object_or_404(Offre, id=offre_id, entreprise=entreprise)

    if request.method == "POST":
        form = OffreForm(request.POST, instance=offre)
        if form.is_valid():
            form.save()
            messages.success(request, f"L'offre « {offre.titre} » a été mise à jour.")
            return redirect("recruteur_mes_offres")
    else:
        form = OffreForm(instance=offre)

    return render(
        request,
        "recruteur/recruteur_poster_offre.html",
        {
            "form": form,
            "active_page": "offres",
            "entreprise": entreprise,
            "editing": True,
            "offre": offre,
        },
    )


@recruteur_required
def recruteur_supprimer_offre(request, offre_id):
    """Supprimer une offre."""
    entreprise = get_entreprise(request.user)
    offre = get_object_or_404(Offre, id=offre_id, entreprise=entreprise)

    if request.method == "POST":
        titre = offre.titre
        offre.delete()
        messages.success(request, f"L'offre « {titre} » a été supprimée.")

    return redirect("recruteur_mes_offres")


@recruteur_required
def recruteur_toggle_offre(request, offre_id):
    """Activer/Désactiver une offre."""
    entreprise = get_entreprise(request.user)
    offre = get_object_or_404(Offre, id=offre_id, entreprise=entreprise)

    if request.method == "POST":
        if offre.statut == "disponible":
            offre.statut = "fermée"
            messages.success(
                request, f"L'offre « {offre.titre} » est maintenant fermée."
            )
        else:
            offre.statut = "disponible"
            messages.success(
                request, f"L'offre « {offre.titre} » est à nouveau disponible."
            )
        offre.save()

    return redirect("recruteur_mes_offres")
