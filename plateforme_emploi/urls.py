from django.contrib import admin

from django.urls import path, include

from django.conf import settings

from django.conf.urls.static import static
from offres.views import home
from users import views as users_views
from offres import admin_views
from offres import recruteur_views


# Liste des URLs principales du projet

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("offres/", include("offres.urls")),
    path("candidatures/", include("candidatures.urls")),
    path("choix_domaine/", users_views.choix_domaine_view, name="choix_domaine"),
    # Dashboard Admin personnalisé
    path("dashboard/", admin_views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/users/", admin_views.admin_users, name="admin_users"),
    path("dashboard/offres/", admin_views.admin_offres, name="admin_offres"),
    path(
        "dashboard/candidatures/",
        admin_views.admin_candidatures,
        name="admin_candidatures",
    ),
    path(
        "dashboard/delete-user/<int:id>/",
        admin_views.admin_delete_user,
        name="admin_delete_user",
    ),
    path(
        "dashboard/delete-offre/<int:id>/",
        admin_views.admin_delete_offre,
        name="admin_delete_offre",
    ),
    path(
        "dashboard/delete-candidature/<int:id>/",
        admin_views.admin_delete_candidature,
        name="admin_delete_candidature",
    ),
    # Espace Recruteur
    path("recruteur/", recruteur_views.recruteur_dashboard, name="recruteur_dashboard"),
    path(
        "recruteur/poster/",
        recruteur_views.recruteur_poster_offre,
        name="recruteur_poster_offre",
    ),
    path(
        "recruteur/mes-offres/",
        recruteur_views.recruteur_mes_offres,
        name="recruteur_mes_offres",
    ),
    path(
        "recruteur/offre/<int:offre_id>/candidatures/",
        recruteur_views.recruteur_candidatures,
        name="recruteur_candidatures",
    ),
    path(
        "recruteur/offre/<int:offre_id>/modifier/",
        recruteur_views.recruteur_modifier_offre,
        name="recruteur_modifier_offre",
    ),
    path(
        "recruteur/offre/<int:offre_id>/supprimer/",
        recruteur_views.recruteur_supprimer_offre,
        name="recruteur_supprimer_offre",
    ),
    path(
        "recruteur/offre/<int:offre_id>/toggle/",
        recruteur_views.recruteur_toggle_offre,
        name="recruteur_toggle_offre",
    ),
]

# Configuration pour servir les fichiers médias pendant le développement
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
