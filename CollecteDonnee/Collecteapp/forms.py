from .models import Capteur
from django import forms

class CapteurForm(forms.ModelForm):
    class Meta:
        model = Capteur
        fields = ['nom_capteur', 'piece']