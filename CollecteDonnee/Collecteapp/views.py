from django.shortcuts import render
from .forms import CapteurForm
from .models import Capteur
from .forms import DonnesForm
from .models import Donnees
from . import models
from django.http import HttpResponseRedirect


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








def liste_donnees(request):
    donnees = Donnees.objects.all()
    return render(request, 'Collecteapp/Donnees/liste_donnees.html', {'donnees': donnees})

def ajouter_donnees(request):
    donnees = Donnees.objects.all()
    if request.method == 'POST':
        form = DonnesForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'Collecteapp/confirmation.html')
    else:
        form = DonnesForm(initial={'donnees': donnees})
    return render(request, 'Collecteapp/Donnees/ajouter_donnees.html', {'form': form, 'donnees': donnees})


def modifier_donnees(request, di):
    capteurs = Capteur.objects.all()
    donnees = models.Donnees.objects.get(pk=di)
    form = DonnesForm(request.POST or None, instance=donnees)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/Collecteapp/Donnees/liste_donnees/")
    else:
        form = DonnesForm(initial={'capteurs': capteurs})
    return render(request, 'Collecteapp/Donnees/modifier_donnees.html', {'form': form, 'capteurs': capteurs, 'capteurs': capteurs})

def supprimer_donnees(request, di):
    donnees = models.Donnees.objects.get(pk=di)
    donnees.delete()
    return render(request, "/Collecteapp/Donnees/liste_donnees/")






import paho.mqtt.client as mqtt
from django.http import HttpResponse
from .models import Donnees

broker = "test.mosquitto.org"
port = 1883
topic = "IUT/Colmar2023/SAE2.04/Maison1"

def parse_received_message(message):
    data = {}
    parts = message.split(",")
    for part in parts:
        key, value = part.split("=")
        data[key.strip()] = value.strip()

    # Add missing keys with default values
    data.setdefault('heure', None)
    data.setdefault('jour', None)
    data.setdefault('temps', None)
    data.setdefault('di', None)

    return data

def on_message(client, userdata, message):
    received_message = str(message.payload.decode("utf-8"))
    print("Message reçu :", received_message)
    
    data = parse_received_message(received_message)
    capteur = Capteur.objects.get(di=data['di'])
    donnees = Donnees(heure=data['heure'], jour=data['jour'], temps=data['temps'], di=capteur)
    donnees.save()


client = mqtt.Client()
client.on_message = on_message
client.connect(broker, port, 60)
client.subscribe(topic)
client.loop_start()

def receive_message(request):
    return HttpResponse("Message reçu !")

