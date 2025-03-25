from django.shortcuts import render
from .models import Parametres
from cours.models import Cours
from entraineurs.models import Entraineur

def accueil(request):
    parametres = Parametres.objects.first()
    cours_populaires = Cours.objects.all()[:4]
    entraineurs = Entraineur.objects.all()[:3]
    
    context = {
        'parametres': parametres,
        'cours_populaires': cours_populaires,
        'entraineurs': entraineurs
    }
    return render(request, 'main/accueil.html', context)