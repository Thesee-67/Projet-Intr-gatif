from .models import Capteur
from .models import Donnees
from django import forms

class CapteurForm(forms.ModelForm):
    class Meta:
        model = Capteur
        fields = "__all__"


class DonnesForm(forms.ModelForm):
    class Meta:
        model = Donnees
        fields = "__all__"
        widgets = {'id_capteur': forms.Select(attrs={'class': 'form-select'}),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_capteur'].widget.choices = [(capteur.id_capteur, capteur.id_capteur) for capteur in Capteur.objects.all()]
 