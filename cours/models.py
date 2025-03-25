class CategorieCours(models.Model):
    nom = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nom

class Cours(models.Model):
    NIVEAUX = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'), 
        ('avance', 'Avancé')
    ]
    
    titre = models.CharField(max_length=100)
    categorie = models.ForeignKey(CategorieCours, on_delete=models.CASCADE)
    description = models.TextField()
    niveau = models.CharField(max_length=20, choices=NIVEAUX)
    duree = models.IntegerField()
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.titre