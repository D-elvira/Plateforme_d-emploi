# On importe forms de Django pour créer des formulaires
from django import forms
# On importe UserCreationForm pour bénéficier du formulaire de création d'utilisateur de Django
from django.contrib.auth.forms import UserCreationForm
# On importe notre modèle utilisateur personnalisé
from .models import User


# formulaire d'inscription
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'role',
            'company_name', 'company_domain', 'company_city', 'company_contact',
            'legal_document',
            'password1', 'password2'
        ]

    # Rendre certains champs optionnels
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_name'].required = False
        self.fields['company_domain'].required = False
        self.fields['company_city'].required = False
        self.fields['company_contact'].required = False
        self.fields['legal_document'].required = False