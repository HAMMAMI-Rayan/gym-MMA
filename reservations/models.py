from django.db import models

class Reservation(models.Model):
    STATUTS = [
        ('confirme', 'Confirmé'),
        ('en_attente', 'En Attente'),
        ('annule', 'Annulé')
    ]
    
    membre = models.ForeignKey(Profil, on_delete=models.CASCADE)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    date_reservation = models.DateTimeField(auto_now_add=True)
    date_cours = models.DateTimeField()
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    
    def __str__(self):
        return f"Réservation de {self.membre.user.username} - {self.cours.titre}"