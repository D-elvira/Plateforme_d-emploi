from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q, Count
from users.models import User
from offres.models import Offre, Entreprise, DA, Candidature
from candidatures.models import Candidature as CandidatureApp


@staff_member_required
def admin_dashboard(request):
    """Tableau de bord principal avec statistiques."""
    total_users = User.objects.count()
    total_candidats = User.objects.filter(role="candidat").count()
    total_recruteurs = User.objects.filter(role="recruteur").count()
    total_offres = Offre.objects.count()
    offres_emploi = Offre.objects.filter(type="emploi").count()
    offres_stage = Offre.objects.filter(type="stage").count()
    offres_disponibles = Offre.objects.filter(statut="disponible").count()
    total_candidatures = Candidature.objects.count()
    total_entreprises = Entreprise.objects.count()

    dernières_offres = Offre.objects.select_related("entreprise").order_by("-id")[:5]
    dernières_candidatures = Candidature.objects.select_related("offre").order_by(
        "-date_envoi"
    )[:5]

    context = {
        "active_page": "dashboard",
        "total_users": total_users,
        "total_candidats": total_candidats,
        "total_recruteurs": total_recruteurs,
        "total_offres": total_offres,
        "offres_emploi": offres_emploi,
        "offres_stage": offres_stage,
        "offres_disponibles": offres_disponibles,
        "total_candidatures": total_candidatures,
        "total_entreprises": total_entreprises,
        "dernieres_offres": dernières_offres,
        "dernieres_candidatures": dernières_candidatures,
    }
    return render(request, "admin/admin_dashboard.html", context)


@staff_member_required
def admin_users(request):
    """Liste de tous les utilisateurs."""
    users = User.objects.all().order_by("-date_joined")
    return render(
        request, "admin/admin_users.html", {"users": users, "active_page": "users"}
    )


@staff_member_required
def admin_offres(request):
    """Liste de toutes les offres."""
    offres = Offre.objects.select_related("entreprise").order_by("-id")
    return render(
        request, "admin/admin_offres.html", {"offres": offres, "active_page": "offres"}
    )


@staff_member_required
def admin_candidatures(request):
    """Liste de toutes les candidatures."""
    candidatures = Candidature.objects.select_related("offre").order_by("-date_envoi")
    return render(
        request,
        "admin/admin_candidatures.html",
        {"candidatures": candidatures, "active_page": "candidatures"},
    )


@staff_member_required
def admin_delete_user(request, id):
    """Supprimer un utilisateur."""
    if request.method == "POST":
        user = get_object_or_404(User, id=id)
        username = user.username
        user.delete()
        messages.success(request, f"L'utilisateur « {username} » a été supprimé.")
    return redirect("admin_users")


@staff_member_required
def admin_delete_offre(request, id):
    """Supprimer une offre."""
    if request.method == "POST":
        offre = get_object_or_404(Offre, id=id)
        titre = offre.titre
        offre.delete()
        messages.success(request, f"L'offre « {titre} » a été supprimée.")
    return redirect("admin_offres")


@staff_member_required
def admin_delete_candidature(request, id):
    """Supprimer une candidature."""
    if request.method == "POST":
        candidature = get_object_or_404(Candidature, id=id)
        candidature.delete()
        messages.success(request, "La candidature a été supprimée.")
    return redirect("admin_candidatures")
