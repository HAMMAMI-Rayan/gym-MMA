from django.db import models
from django.contrib.auth.models import User

class Coach(models.Model):
    """
    Modèle pour les entraîneurs de MMA
    Relation 1:1 avec User pour l'authentification
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100)
    experience = models.IntegerField(help_text="Années d'expérience")
    bio = models.TextField()
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.speciality}"

class Course(models.Model):
    """
    Modèle pour les cours de MMA
    Relation N:1 avec Coach
    """
    LEVEL_CHOICES = [
        ('BEG', 'Débutant'),
        ('INT', 'Intermédiaire'),
        ('ADV', 'Avancé'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='courses')
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES)
    max_students = models.IntegerField()
    schedule = models.CharField(max_length=100, help_text="Jour et heure du cours")
    
    def __str__(self):
        return f"{self.name} ({self.get_level_display()}) - {self.coach}"

class Member(models.Model):
    """
    Modèle pour les membres de la salle
    Relation 1:1 avec User pour l'authentification
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=100)
    medical_info = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Enrollment(models.Model):
    """
    Modèle pour les inscriptions aux cours
    Relation N:N entre Member et Course
    """
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    date_enrolled = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        # Contrainte unique pour éviter les doublons d'inscriptions
        unique_together = ('member', 'course')
    
    def __str__(self):
        return f"{self.member} inscrit à {self.course}"