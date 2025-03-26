from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Coach, Course, Member, Enrollment
from .forms import UserRegisterForm, MemberForm, CoachForm, CourseForm, EnrollmentForm

def index(request):
    """Vue pour la page d'accueil"""
    return render(request, 'gym/index.html', {
        'coach_count': Coach.objects.count(),
        'course_count': Course.objects.count(),
        'member_count': Member.objects.count(),
    })

def register(request):
    """Vue pour l'inscription d'un nouveau membre"""
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        member_form = MemberForm(request.POST)
        if user_form.is_valid() and member_form.is_valid():
            user = user_form.save()
            member = member_form.save(commit=False)
            member.user = user
            member.save()
            messages.success(request, "Compte créé avec succès! Vous pouvez maintenant vous connecter.")
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        member_form = MemberForm()
    
    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'member_form': member_form,
    })

@login_required
def profile(request):
    """Vue pour afficher et mettre à jour le profil de l'utilisateur"""
    try:
        member = request.user.member
        is_coach = False
    except Member.DoesNotExist:
        try:
            member = request.user.coach
            is_coach = True
        except Coach.DoesNotExist:
            # Ni membre ni coach
            return redirect('index')
    
    if request.method == 'POST':
        if is_coach:
            form = CoachForm(request.POST, instance=member)
        else:
            form = MemberForm(request.POST, instance=member)
            
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès!")
            return redirect('profile')
    else:
        if is_coach:
            form = CoachForm(instance=member)
        else:
            form = MemberForm(instance=member)
    
    return render(request, 'gym/profile.html', {
        'form': form,
        'is_coach': is_coach,
    })

@login_required
def enroll_course(request):
    """Vue pour s'inscrire à un cours"""
    # Vérifier si l'utilisateur est un membre
    try:
        member = request.user.member
    except Member.DoesNotExist:
        messages.error(request, "Seuls les membres peuvent s'inscrire aux cours.")
        return redirect('index')
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.member = member
            
            # Vérifier si le membre est déjà inscrit à ce cours
            if Enrollment.objects.filter(member=member, course=enrollment.course).exists():
                messages.error(request, "Vous êtes déjà inscrit à ce cours.")
            else:
                # Vérifier si le cours n'est pas complet
                current_enrollments = Enrollment.objects.filter(course=enrollment.course, is_active=True).count()
                if current_enrollments < enrollment.course.max_students:
                    enrollment.save()
                    messages.success(request, f"Inscription réussie au cours {enrollment.course.name}!")
                else:
                    messages.error(request, "Ce cours est complet, veuillez en choisir un autre.")
            
            return redirect('enrollment')
    else:
        form = EnrollmentForm()
    
    # Obtenir la liste des inscriptions actuelles
    enrollments = Enrollment.objects.filter(member=member, is_active=True)
    
    return render(request, 'gym/enrollment.html', {
        'form': form,
        'enrollments': enrollments,
    })

# Vues génériques pour les entraîneurs (CRUD)
class CoachListView(ListView):
    model = Coach
    template_name = 'gym/coach_list.html'
    context_object_name = 'coaches'

class CoachDetailView(DetailView):
    model = Coach
    template_name = 'gym/coach_detail.html'

class CoachCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Coach
    form_class = CoachForm
    template_name = 'gym/coach_form.html'
    success_url = reverse_lazy('coach-list')
    
    def test_func(self):
        # Seul un super-utilisateur peut ajouter un entraîneur
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        # Associer le coach à l'utilisateur existant
        coach = form.save(commit=False)
        coach.user = self.request.user
        return super().form_valid(form)

class CoachUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Coach
    form_class = CoachForm
    template_name = 'gym/coach_form.html'
    success_url = reverse_lazy('coach-list')
    
    def test_func(self):
        coach = self.get_object()
        return self.request.user == coach.user or self.request.user.is_superuser

class CoachDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Coach
    template_name = 'gym/coach_confirm_delete.html'
    success_url = reverse_lazy('coach-list')
    
    def test_func(self):
        # Seul un super-utilisateur peut supprimer un entraîneur
        return self.request.user.is_superuser

# Vues génériques pour les cours (CRUD)
class CourseListView(ListView):
    model = Course
    template_name = 'gym/course_list.html'
    context_object_name = 'courses'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'gym/course_detail.html'

class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'gym/course_form.html'
    success_url = reverse_lazy('course-list')
    
    def test_func(self):
        # Seul un entraîneur ou un superuser peut créer un cours
        try:
            return hasattr(self.request.user, 'coach') or self.request.user.is_superuser
        except:
            return False

class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'gym/course_form.html'
    success_url = reverse_lazy('course-list')
    
    def test_func(self):
        course = self.get_object()
        # Seul l'entraîneur du cours ou un superuser peut le modifier
        return self.request.user == course.coach.user or self.request.user.is_superuser

class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    template_name = 'gym/course_confirm_delete.html'
    success_url = reverse_lazy('course-list')
    
    def test_func(self):
        course = self.get_object()
        # Seul l'entraîneur du cours ou un superuser peut le supprimer
        return self.request.user == course.coach.user or self.request.user.is_superuser