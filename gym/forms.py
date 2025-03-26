from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Coach, Course, Member, Enrollment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['date_of_birth', 'address', 'phone', 'emergency_contact', 'medical_info']

class CoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = ['speciality', 'experience', 'bio', 'phone']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'coach', 'level', 'max_students', 'schedule']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course']