# On importe AbstractUser pour créer un modèle utilisateur personnalisé
from django.contrib.auth.models import AbstractUser
# définition des champs de notre modèle
from django.db import models

# héritage de AbstractUser
class User(AbstractUser):
    # Définition des rôles possibles pour un utilisateur
    #(valeur_en_base, valeur_affichée)
    ROLE_CHOICES = (
        ('candidat', 'Candidat'),
        ('entreprise', 'Entreprise'),
    )
    # CharField → chaîne de caractères
    # max_length=20 → longueur maximale de 20 caractères
    # choices=ROLE_CHOICES → l'utilisateur doit avoir un rôle parmi ceux définis ci-dessus
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
