from django.urls import path
from . import views  # On importe les vues de l'app "offres"

urlpatterns = [
    path('', views.offres_list, name='offres_list'),  # Exemple de route
    path('<int:id>/', views.offre_detail, name='offre_detail'),  # Détail d'une offre
]
