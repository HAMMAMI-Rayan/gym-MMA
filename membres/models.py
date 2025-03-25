from django.contrib.auth.models import User
from django.db import models

class Profil(models.Model):
    NIVEAUX_MMA = [
        ('debutant', 'Débutant'),
        ('amateur', 'Amateur'),
        ('pro', 'Professionnel')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_naissance = models.DateField()
    niveau_mma = models.CharField(max_length=20, choices=NIVEAUX_MMA)
    date_inscription = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username