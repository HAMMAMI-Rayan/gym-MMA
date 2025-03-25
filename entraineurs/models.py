class Entraineur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='entraineurs/')
    annees_experience = models.IntegerField()
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"