from django.db import models

class Parametres(models.Model):
    nom_salle = models.CharField(max_length=100)
    description = models.TextField()
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    horaires_ouverture = models.TextField()