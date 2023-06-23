from django.shortcuts import render, redirect
from .forms import CapteurForm
from .models import Capteur
from .forms import DonnesForm
from .models import Donnees
from . import models
import matplotlib.pyplot as plt
from django.http import HttpResponseRedirect
from datetime import datetime
from django.db.models import Q


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
            return render(request, 'Collecteapp/Capteur/confirmation.html')
    else:
        form = CapteurForm()    
    return render(request, 'Collecteapp/Capteur/ajouter_capteur.html',{'form': form})

# Only for prod
def modifier_capteur(request, id_capteur):
    capteurs = Capteur.objects.get(pk=id_capteur)
    form = CapteurForm(request.POST or None, instance=capteurs)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/Collecteapp/Capteur/liste_capteur/")

    return render(request, 'Collecteapp/Capteur/modifier_capteur.html', {'form': form, 'capteurs': capteurs})


def supprimer_capteur(request, id_capteur):
    capteurs = Capteur.objects.get(pk=id_capteur)
    return render(request, "Collecteapp/Capteur/supprimer_capteur.html", {"capteurs": capteurs})

def supprimer_confirm_capteur(request, id_capteur):
    capteurs = Capteur.objects.get(pk=id_capteur)
    capteurs.delete()
    return HttpResponseRedirect("/Collecteapp/Capteur/liste_capteur/")

def liste_donnees(request):
    donnees = Donnees.objects.all()
    return render(request, 'Collecteapp/Donnees/liste_donnees.html', {'donnees': donnees})

def ajouter_donnees(request):
    capteurs = Capteur.objects.all()
    if request.method == 'POST':
        form = DonnesForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'Collecteapp/Donnees/confirmation_donnees.html')
    else:
        form = DonnesForm(initial={'capteurs': capteurs})
    return render(request, 'Collecteapp/Donnees/ajouter_donnees.html', {'form': form, 'capteurs': capteurs})

def modifier_donnees(request, id):
    capteurs = Capteur.objects.all()
    donnees = Donnees.objects.get(pk=id)
    if request.method == 'POST':
        form = DonnesForm(request.POST, instance=donnees)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/Donnees/liste_donnees/')
    else:
        form = DonnesForm(instance=donnees, initial={'capteurs': capteurs})
    return render(request, 'Collecteapp/Donnees/modifier_donnees.html', {'form': form, 'capteurs': capteurs, 'donnees': donnees})

def supprimer_donnees(request, id):
    donnees = models.Donnees.objects.get(pk=id)
    return render(request,"Collecteapp/Donnees/supprimer_donnees.html", {"donnees": donnees})

def supprimer_confirm_donnees(request, id):
    donnees = models.Donnees.objects.get(pk=id)
    donnees.delete()
    return HttpResponseRedirect("/Collecteapp/Donnees/liste_donnees/")

def Graphique(request):
    form = DonnesForm()

    if request.method == 'POST':
        form = DonnesForm(request.POST)
        if form.is_valid():
            id_capteur = form.cleaned_data['id_capteur']

            # Récupérer les données du capteur depuis la base de données
            donnees = Donnees.objects.filter(id_capteur=id_capteur)

            # Préparer les données pour le graphique
            labels = [str(donnee.date) for donnee in donnees]
            temps = [donnee.temps for donnee in donnees]

            # Créer un graphique
            plt.plot(labels, temps)
            plt.title('Graphique des données')
            plt.xlabel('Date')
            plt.ylabel('Temps')

            # Convertir le graphique en image
            image_path = '/static/image/graphique.png'  # Chemin vers l'image
            plt.savefig(image_path)

            # Renvoyer les données au template
            context = {
                'form': form,
                'chart_image': image_path,
            }
            return render(request, 'Collecteapp/graphique.html', context)

    context = {
        'form': form,
    }
    return render(request, 'Collecteapp/graphique.html', context)


def liste_dates(request):
    if request.method == 'POST':
        date_start_str = request.POST.get('date_start')
        heure_start_str = request.POST.get('heure_start')
        date_end_str = request.POST.get('date_end')
        heure_end_str = request.POST.get('heure_end')

        if not date_start_str or not heure_start_str or not date_end_str or not heure_end_str:
            return render(request, 'Collecteapp/Donnees/date_invalide.html')

        try:
            datetime_start = datetime.strptime(date_start_str + heure_start_str, '%d/%m/%Y%H:%M:%S')
            datetime_end = datetime.strptime(date_end_str + heure_end_str, '%d/%m/%Y%H:%M:%S')
        except ValueError:
            return render(request, 'Collecteapp/Donnees/date_invalide.html')

        donnees = Donnees.objects.filter(
            Q(date__gt=datetime_start.date()) | (Q(date=datetime_start.date()) & Q(time__gte=datetime_start.time())),
            Q(date__lt=datetime_end.date()) | (Q(date=datetime_end.date()) & Q(time__lte=datetime_end.time()))
        )

        if donnees:
            context = {
                'donnees': donnees,
                'datetime_start': datetime_start,
                'datetime_end': datetime_end,
            }
            return render(request, 'Collecteapp/Donnees/liste_donnees_date.html', context)
        else:
            return render(request, 'Collecteapp/Donnees/retour.html')

    return render(request, 'Collecteapp/Donnees/liste_donnees_date.html')



