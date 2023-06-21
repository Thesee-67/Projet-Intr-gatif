from django.shortcuts import render
from .forms import CollecteForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import Collecte
from django.shortcuts import get_object_or_404

def main(request):
    return render(request, 'CollecteDonnee/main.html')

def ajout(request):
    if request.method == 'POST':
        form = CollecteForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'CollecteDonnee/affiche.html')
    else:
        form = CollecteForm()
    
    return render(request, 'CollecteDonnee/ajout.html', {'form': form})

def traitement(request):
    lform = CollecteForm(request.POST)
    if lform.is_valid():
        collecte = lform.save()
        return render(request, 'CollecteDonnee/affiche.html', {'collecte': collecte})
    else:
        return render(request, 'CollecteDonnee/ajout.html', {'form': lform})

def affiche(request):
    collectes = Collecte.objects.all()
    return render(request, 'CollecteDonnee/affiche.html', {'collectes': collectes})

def read(request, id):
    collecte = get_object_or_404(Collecte, pk=id)
    return render(request, 'CollecteDonnee/affiche.html', {'collecte': collecte})

def traitementupdate(request, id):
    lform = CollecteForm(request.POST)
    if lform.is_valid():
        collecte = lform.save(commit=False)
        collecte.id = id
        collecte.save()
        return HttpResponseRedirect("/CollecteDonnee/affiche/")
    else:
        return render(request, 'CollecteDonnee/update.html', {'form': lform, 'id': id})

def update(request, id):
    collecte = get_object_or_404(Collecte, pk=id)
    form = CollecteForm(instance=collecte)
    return render(request, 'CollecteDonnee/update.html', {'form': form, 'id': id})

def delete(request, id):
    collecte = get_object_or_404(Collecte, pk=id)
    collecte.delete()
    return HttpResponseRedirect("/CollecteDonnee/affiche/")
