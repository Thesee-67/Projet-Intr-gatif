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
import io
import json
from django.http import HttpResponse
import csv
from rest_framework import generics
from .serializers import ModelSerializer



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

def modifier_capteur(request, id_capteur):
    capteur = Capteur.objects.get(pk=id_capteur)
    form = CapteurForm(request.POST or None, instance=capteur)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/Collecteapp/Capteur/liste_capteur/")
    else:
        form = CapteurForm(instance=capteur)

    return render(request, 'Collecteapp/Capteur/modifier_capteur.html', {'form': form, 'capteur': capteur})


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



def filtrer_par_capteur(request):
    capteurs = Capteur.objects.all()

    if request.method == 'POST':
        id_capteur = request.POST.get('id_capteur')

        if not id_capteur:
            return render(request, 'Collecteapp/Donnees/filtre_capteur.html', {'erreur': 'Veuillez choisir un capteur à filtrer.'})

        try:
            capteur = Capteur.objects.get(id_capteur=id_capteur)
        except Capteur.DoesNotExist:
            return render(request, 'Collecteapp/Donnees/filtre_capteur.html', {'erreur': 'Le capteur spécifié n\'existe pas.'})

        donnees = Donnees.objects.filter(id_capteur=capteur)

        context = {
            'donnees': donnees,
            'capteur': capteur,
            'capteurs': capteurs
        }

        return render(request, 'Collecteapp/Donnees/filtre_capteur.html', context)

    context = {
        'capteurs': capteurs
    }

    return render(request, 'Collecteapp/Donnees/filtre_capteur.html', context)

def filtrer_donnees(request):
    capteurs = Capteur.objects.all()

    if request.method == 'POST':
        date_start_str = request.POST.get('date_start')
        heure_start_str = request.POST.get('heure_start')
        date_end_str = request.POST.get('date_end')
        heure_end_str = request.POST.get('heure_end')
        id_capteur = request.POST.get('id_capteur')

        if not date_start_str or not heure_start_str or not date_end_str or not heure_end_str:
            return render(request, 'Collecteapp/Donnees/date_invalide.html')

        if not id_capteur:
            return render(request, 'Collecteapp/Donnees/filtre_capteur.html', {'erreur': 'Veuillez choisir un capteur à filtrer.'})

        try:
            datetime_start = datetime.strptime(date_start_str + heure_start_str, '%d/%m/%Y%H:%M:%S')
            datetime_end = datetime.strptime(date_end_str + heure_end_str, '%d/%m/%Y%H:%M:%S')
        except ValueError:
            return render(request, 'Collecteapp/Donnees/date_invalide.html')

        try:
            capteur = Capteur.objects.get(id_capteur=id_capteur)
        except Capteur.DoesNotExist:
            return render(request, 'Collecteapp/Donnees/filtre_capteur.html', {'erreur': 'Le capteur spécifié n\'existe pas.'})

        donnees = Donnees.objects.filter(
            Q(date__gt=datetime_start.date()) | (Q(date=datetime_start.date()) & Q(time__gte=datetime_start.time())),
            Q(date__lt=datetime_end.date()) | (Q(date=datetime_end.date()) & Q(time__lte=datetime_end.time())),
            id_capteur=capteur
        )

        if donnees:
            context = {
                'donnees': donnees,
                'datetime_start': datetime_start,
                'datetime_end': datetime_end,
                'capteur': capteur,
                'capteurs': capteurs
            }
            return render(request, 'Collecteapp/Donnees/filtre_donnees.html', context)
        else:
            return render(request, 'Collecteapp/Donnees/retour.html')

    context = {
        'capteurs': capteurs
    }

    return render(request, 'Collecteapp/Donnees/filtre_donnees.html', context)

def generate_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Colonne1', 'Colonne2', 'Colonne3', 'Colonne4'])

    data = Donnees.objects.all()
    for item in data:
        writer.writerow([item.id_capteur, item.date, item.time,item.temps])

    return response

def supprimer_toutes_donnees(request):
    donnees = Donnees.objects.all
    return render(request,"Collecteapp/Donnees/supprimer_tout.html", {"donnees": donnees})

def supprimer_confirm_toutes_donnees(request):
    Donnees.objects.all().delete()
    return HttpResponseRedirect("/Collecteapp/Donnees/liste_donnees/")

def selection_capteurs(request):
    capteurs = Capteur.objects.all()
    context = {
        'capteurs': capteurs
    }
    return render(request, 'Collecteapp/selection_capteurs.html', context)

def graphique(request):
    capteur_id = request.GET.get('capteur')
    capteur = Capteur.objects.get(id_capteur=capteur_id)
    donnees = Donnees.objects.filter(id_capteur=capteur_id)

    date = [str(donnee.date) for donnee in donnees]
    time = [str(donnee.time) for donnee in donnees]
    temps = [donnee.temps for donnee in donnees]

    context = {
        'capteur': capteur,
        'date': json.dumps(date),
        'time': json.dumps(time),
        'temps': json.dumps(temps),
    }

    return render(request, 'Collecteapp/graphique.html', context)

def contact(request):
    return render(request, 'Collecteapp/contact.html')


class ModelList(generics.ListCreateAPIView):
    queryset = Donnees.objects.all()
    serializer_class = ModelSerializer

class ModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donnees.objects.all()
    serializer_class = ModelSerializer


