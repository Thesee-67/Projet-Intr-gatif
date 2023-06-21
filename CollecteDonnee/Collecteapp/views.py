from django.shortcuts import render
from .forms import CapteurForm
from .models import Capteur
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request, 'Collecteapp/index.html')

# aeroport
def liste_capteurs(request):
    capteurs = Capteur.objects.all()
    return render(request, 'Collecteapp/Capteur/liste_capteur.html', {'capteurs': capteurs})

# Only for prod
def modifier_capteur(request, id):
    capteurs = Capteur.objects.get(pk=id)
    form = CapteurForm(request.POST or None, instance=capteurs)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/Collecteapp/Capteur/liste")
    return render(request, 'Collecteapp/Capteur/modifier_capteur.html', {'form': form, 'capteurs': capteurs})
