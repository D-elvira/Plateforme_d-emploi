
from django import forms
from candidatures.models import Candidature

class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['nom_complet', 'email', 'cv', 'message']