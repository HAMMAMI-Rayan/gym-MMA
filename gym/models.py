from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_coach = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {'Coach' if self.is_coach else 'Membre'}"


class Course(models.Model):
    COURSE_TYPES = [
        ('boxing', 'Boxe'),
        ('bjj', 'Jiu-Jitsu Brésilien'),
        ('wrestling', 'Lutte'),
        ('mma', 'MMA'),
        ('thai', 'Boxe Thaï'),
        ('conditioning', 'Préparation Physique'),
    ]
    
    LEVELS = [
        ('beginner', 'Débutant'),
        ('intermediate', 'Intermédiaire'),
        ('advanced', 'Avancé'),
        ('all', 'Tous niveaux'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    course_type = models.CharField(max_length=20, choices=COURSE_TYPES)
    level = models.CharField(max_length=20, choices=LEVELS)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_participants = models.PositiveIntegerField(default=20)
    
    def __str__(self):
        return f"{self.title} - {self.get_course_type_display()} - {self.date}"
    
    def get_available_spots(self):
        return self.max_participants - self.reservations.count()
    
    def is_full(self):
        return self.get_available_spots() <= 0
    
    def is_upcoming(self):
        return timezone.now().date() <= self.date


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reservations')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'course']
        
    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.course.date}"