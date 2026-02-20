from django import forms
from offres.models import Offre


class OffreForm(forms.ModelForm):
    """Formulaire pour créer/modifier une offre."""

    class Meta:
        model = Offre
        fields = ["titre", "type", "categorie", "ville", "profil_recherche", "attentes"]
        widgets = {
            "titre": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all",
                    "placeholder": "Ex: Développeur Full Stack Junior",
                }
            ),
            "type": forms.Select(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all",
                }
            ),
            "categorie": forms.Select(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all",
                }
            ),
            "ville": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all",
                    "placeholder": "Ex: Douala",
                }
            ),
            "profil_recherche": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all",
                    "rows": 4,
                    "placeholder": "Décrivez le profil idéal du candidat...",
                }
            ),
            "attentes": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all",
                    "rows": 4,
                    "placeholder": "Compétences, diplômes, expérience requise...",
                }
            ),
        }
        labels = {
            "titre": "Titre de l'offre",
            "type": "Type d'offre",
            "categorie": "Catégorie",
            "ville": "Ville",
            "profil_recherche": "Profil recherché",
            "attentes": "Attentes & compétences",
        }
