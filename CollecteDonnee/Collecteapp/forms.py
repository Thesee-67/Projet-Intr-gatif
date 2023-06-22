from .models import Capteur
from .models import Donnees
from django import forms

class CapteurForm(forms.ModelForm):
    class Meta:
        model = Capteur
        fields = ['di', 'piece']


class DonnesForm(forms.ModelForm):
    class Meta:
        model = Donnees
        fields = ['heure','jour', 'temps', 'capteur']
        widgets = {'capteur': forms.Select(attrs={'class': 'form-select'}),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['capteur'].widget.choices = [(capteur.piece, capteur.di) for capteur in Capteur.objects.all()]

 