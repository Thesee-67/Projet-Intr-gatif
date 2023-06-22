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


def ajouter_capteur(request):
    if request.method == 'POST':
        form = CapteurForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'Collecteapp/confirmation.html')
    else:
        form = CapteurForm()

    return render(request, 'Collecteapp/Capteur/ajouter_capteur.html',{'form': form})

# Only for prod
def modifier_capteur(request, di):
    capteurs = Capteur.objects.get(pk=di)
    form = CapteurForm(request.POST or None, instance=capteurs)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/Collecteapp/Capteur/liste_capteur")
    return render(request, 'Collecteapp/Capteur/modifier_capteur.html', {'form': form, 'capteurs': capteurs})


def supprimer_capteur(request, di):
    capteurs = Capteur.objects.get(pk=di)
    return render(request, "Collecteapp/Capteur/supprimer_capteur.html", {"capteurs": capteurs})


def supprimer_confirm_capteur(request, di):
    capteurs = Capteur.objects.get(pk=di)
    capteurs.delete()
    return HttpResponseRedirect("/Collecteapp/Capteur/liste_capteur/")