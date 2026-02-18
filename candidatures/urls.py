from django.urls import path
from . import views  # On importe les vues

urlpatterns = [
    path('', views.candidatures_list, name='candidatures_list'),
]
