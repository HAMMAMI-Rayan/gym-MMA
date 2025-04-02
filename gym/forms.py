from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Course, Reservation


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    is_coach = forms.BooleanField(required=False, label='Je suis un coach')
    phone_number = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            
            # Création du profil utilisateur
            UserProfile.objects.create(
                user=user,
                is_coach=self.cleaned_data.get('is_coach', False),
                phone_number=self.cleaned_data.get('phone_number', '')
            )
            
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'bio', 'photo']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'course_type', 'level', 'date', 
                  'start_time', 'end_time', 'max_participants']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("L'heure de fin doit être ultérieure à l'heure de début.")
        
        return cleaned_data


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['course']
        widgets = {
            'course': forms.HiddenInput()
        }