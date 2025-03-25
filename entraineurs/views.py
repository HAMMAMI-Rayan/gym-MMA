from django.shortcuts import render

def liste_entraineurs(request):
    entraineurs = Entraineur.objects.all()
    return render(request, 'entraineurs/liste_entraineurs.html', {'entraineurs': entraineurs})
