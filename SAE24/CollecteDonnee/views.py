from django.shortcuts import render
from .forms import CollecteForm

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
        examens = lform.save()
        return render(request, 'CollecteDonnee/affiche.html', {'examens': examens})
    else:
        return render(request, 'CollecteDonnee/ajout.html', {'form': lform})