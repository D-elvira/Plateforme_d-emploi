# On importe AbstractUser pour créer un modèle utilisateur personnalisé
from django.contrib.auth.models import AbstractUser
# définition des champs de notre modèle
from django.db import models

# héritage de AbstractUser
class User(AbstractUser):
    ROLE_CHOICES = (
        ('candidat', 'Candidat'),
        ('recruteur', 'Recruteur'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Champs spécifiques aux recruteurs
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_domain = models.CharField(max_length=255, blank=True, null=True)
    company_city = models.CharField(max_length=100, blank=True, null=True)
    company_contact = models.CharField(max_length=100, blank=True, null=True)
    legal_document = models.FileField(upload_to='legal_docs/', blank=True, null=True)