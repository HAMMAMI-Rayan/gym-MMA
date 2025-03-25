from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import Profil

def inscription(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        niveau_mma = request.POST['niveau_mma']

        user = User.objects.create_user(username=username, email=email, password=password)
        profil = Profil.objects.create(
            user=user, 
            niveau_mma=niveau_mma,
            date_naissance=None  # À compléter
        )
        login(request, user)
        return redirect('accueil')
    return render(request, 'membres/inscription.html')