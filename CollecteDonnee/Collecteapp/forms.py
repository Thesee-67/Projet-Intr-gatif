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
 