from django.db import models

from users.models import User

class DA(models.Model):
    # Nom du domaine d'activité
    nom = models.CharField(max_length=100)

    # Méthode qui permet d'afficher le nom du DA dans l'admin ou lors d'une impression
    def __str__(self):
        return self.nom


class Entreprise(models.Model):
    # Chaque entreprise correspond à un seul utilisateur
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200)
    ville = models.CharField(max_length=100)
    domaine = models.CharField(max_length=200)
    legal_info = models.ImageField(upload_to='logos_entreprises/', null=True, blank=True)

class Offre(models.Model):
    TYPE_CHOICES = (
        ('emploi', 'Emploi'),  # Offre d'emploi
        ('stage', 'Stage'),  # Offre de stage
    )
    CATEGORIE_CHOICES = (
        ('academique', 'Stage académique'),  # Stage lié aux études
        ('professionnel', 'Stage professionnel'),  # Stage en entreprise
        ('poste', 'Poste de travail'),  # Poste permanent
    )
    # Une entreprise peut avoir plusieurs offres
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    # Titre de l'offre
    titre = models.CharField(max_length=200)
    # Type d'offre (emploi ou stage)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    # Catégorie de l'offre
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    # Profil recherché pour le poste/stage
    profil_recherche = models.TextField()
    # Attentes de l'entreprise (compétences, diplômes…)
    attentes = models.TextField()
    # Ville où se situe l'offre
    ville = models.CharField(max_length=100)
    # Statut de l'offre (par défaut : disponible)
    statut = models.CharField(max_length=20, default='disponible')


class Candidature(models.Model):
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE, related_name='candidatures')
    nom_complet = models.CharField(max_length=200)
    email = models.EmailField()
    cv = models.FileField(upload_to='cv_candidats/')
    message = models.TextField(blank=True)
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Candidature de {self.nom_complet} pour {self.offre.titre}"