from django.db import models
from users.models import User
from offres.models import Offre

class Candidature(models.Model):
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    candidat = models.ForeignKey(User, on_delete=models.CASCADE)
    cv = models.FileField(upload_to='cvs/')
    date_postulation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, default='en attente')
