from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Collecte

class CollecteForm(forms.ModelForm):
    class Meta:
        model = Collecte
        fields = ('id','idcollecte' ,'piece', 'date', 'heure', 'temp')
        labels = {
            'id':_('ID'),
            'idcollecte': _('idcollecte'),
            'piece': _('Pièce'),
            'date': _('Date'),
            'heure': _('Heure'),
            'temp': _('Température'),
        }

