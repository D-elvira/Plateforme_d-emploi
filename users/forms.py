# On importe forms de Django pour créer des formulaires
from django import forms
# On importe UserCreationForm pour bénéficier du formulaire de création d'utilisateur de Django
from django.contrib.auth.forms import UserCreationForm
# On importe notre modèle utilisateur personnalisé
from .models import User


# formulaire d'inscription
class UserRegisterForm(UserCreationForm):
    # Classe Meta pour configurer le formulaire
    class Meta:
        model = User  # Le formulaire va créer/modifier des instances du modèle User
        # 'password1' et 'password2' : pour saisir et confirmer le mot de passe
        fields = ['username', 'email', 'role', 'password1', 'password2']
