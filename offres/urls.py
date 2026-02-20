from django.urls import path
from . import views  # On importe les vues de l'app "offres"

urlpatterns = [
    path("", views.offres_list, name="offres_list"),
    path("recherche/", views.recherche_intelligente, name="recherche_intelligente"),
    path("mes-candidatures/", views.mes_candidatures, name="mes_candidatures"),
    path("<int:id>/", views.offre_detail, name="offre_detail"),
]
