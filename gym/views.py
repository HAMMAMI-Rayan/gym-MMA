from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth import logout
from .models import UserProfile, Course, Reservation
from .forms import UserRegistrationForm, UserProfileForm, CourseForm, ReservationForm
from .models import Course, UserProfile, Reservation


def home(request):
    upcoming_courses = Course.objects.filter(date__gte=timezone.now().date()).order_by('date', 'start_time')[:5]
    return render(request, 'home.html', {'upcoming_courses': upcoming_courses})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour {username}! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


# Fonction de déconnexion personnalisée
def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès!')
    return redirect('home')


@login_required
def profile(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    user_reservations = Reservation.objects.filter(user=request.user).order_by('course__date')
    
    return render(request, 'gym/profile.html', {
        'form': form,
        'profile': profile,
        'reservations': user_reservations
    })


class CourseListView(ListView):
    model = Course
    template_name = 'gym/course_list.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        queryset = Course.objects.filter(date__gte=timezone.now().date()).order_by('date', 'start_time')
        
        # Filtrage par type de cours
        course_type = self.request.GET.get('type')
        if course_type:
            queryset = queryset.filter(course_type=course_type)
            
        # Filtrage par niveau
        level = self.request.GET.get('level')
        if level:
            queryset = queryset.filter(level=level)
            
        # Filtrage par date
        date = self.request.GET.get('date')
        if date:
            queryset = queryset.filter(date=date)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_types'] = Course.COURSE_TYPES
        context['levels'] = Course.LEVELS
        return context



class CoachRequiredMixin(UserPassesTestMixin):
    """Mixin pour restreindre l'accès aux coachs uniquement"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.profile.is_coach


class CourseCreateView(LoginRequiredMixin, CoachRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'gym/course_form.html'
    success_url = reverse_lazy('course_list')
    
    def form_valid(self, form):
        form.instance.coach = self.request.user
        messages.success(self.request, 'Le cours a été créé avec succès!')
        return super().form_valid(form)


class CourseUpdateView(LoginRequiredMixin, CoachRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'gym/course_form.html'
    success_url = reverse_lazy('course_list')
    
    def test_func(self):
        """Vérifie si l'utilisateur est le coach du cours"""
        return super().test_func() and self.get_object().coach == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Le cours a été mis à jour avec succès!')
        return super().form_valid(form)


class CourseDeleteView(LoginRequiredMixin, CoachRequiredMixin, DeleteView):
    model = Course
    template_name = 'gym/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')
    
    def test_func(self):
        """Vérifie si l'utilisateur est le coach du cours"""
        return super().test_func() and self.get_object().coach == self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Le cours a été supprimé avec succès!')
        return super().delete(request, *args, **kwargs)


@login_required
def reserve_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Vérifier si le cours est complet
    if course.is_full():
        messages.error(request, 'Désolé, ce cours est complet.')
        return redirect('course_detail', pk=course_id)
    
    # Vérifier si l'utilisateur a déjà réservé ce cours
    existing_reservation = Reservation.objects.filter(user=request.user, course=course).exists()
    if existing_reservation:
        messages.info(request, 'Vous avez déjà réservé ce cours.')
        return redirect('course_detail', pk=course_id)
    
    # Créer la réservation
    try:
        Reservation.objects.create(user=request.user, course=course)
        messages.success(request, 'Votre réservation a été effectuée avec succès!')
    except IntegrityError:
        messages.error(request, 'Une erreur est survenue lors de la réservation.')
    
    return redirect('course_detail', pk=course_id)



class CoachDashboardView(LoginRequiredMixin, CoachRequiredMixin, ListView):
    model = Course
    template_name = 'gym/coach_dashboard.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        return Course.objects.filter(coach=self.request.user).order_by('date', 'start_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer les réservations pour les cours du coach
        coach_courses = self.get_queryset()
        course_ids = coach_courses.values_list('id', flat=True)
        reservations = Reservation.objects.filter(course_id__in=course_ids)
        
        # Créer un dictionnaire {course_id: nombre de réservations}
        reservation_counts = {}
        for course_id in course_ids:
            reservation_counts[course_id] = reservations.filter(course_id=course_id).count()
            
        context['reservation_counts'] = reservation_counts
        return context


# Fonction de déconnexion personnalisée
def logout_view(request):
    # Vérifier que la méthode est soit GET soit POST
    if request.method in ['GET', 'POST']:
        logout(request)
        messages.success(request, 'Vous avez été déconnecté avec succès!')
    return redirect('home')

@login_required
def reserve_course(request, course_id):
    """Vue pour réserver un cours"""
    course = get_object_or_404(Course, id=course_id)
    
    # Vérifier si l'utilisateur a déjà réservé ce cours
    if Reservation.objects.filter(user=request.user, course=course).exists():
        messages.info(request, 'Vous avez déjà réservé ce cours.')
    else:
        # Créer la réservation
        Reservation.objects.create(user=request.user, course=course)
        messages.success(request, 'Votre réservation a été effectuée avec succès!')
    
    return redirect('course-detail', pk=course_id)


@login_required
def cancel_reservation(request, reservation_id):
    """Vue pour annuler une réservation"""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    course = reservation.course
    
    # Supprimer la réservation
    reservation.delete()
    
    # Calculer le nombre de places disponibles après annulation
    current_reservations = Reservation.objects.filter(course=course).count()
    remaining_spots = course.max_participants - current_reservations
    
    messages.success(request, f'Votre réservation a été annulée avec succès! Il y a maintenant {remaining_spots} places disponibles.')
    
    return redirect('course-detail', pk=course.id)

class CourseDetailView(DetailView):
    model = Course
    template_name = 'gym/course_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Vérifier si l'utilisateur est connecté
        user_has_reservation = False
        reservation = None
        
        # Calculer les places disponibles
        total_spots = self.object.max_participants
        reserved_spots = Reservation.objects.filter(course=self.object).count()
        available_spots = total_spots - reserved_spots
        
        # Calculer le pourcentage de remplissage
        fill_percentage = int((reserved_spots / total_spots) * 100) if total_spots > 0 else 0
        
        if self.request.user.is_authenticated:
            # Vérifier si l'utilisateur a déjà réservé ce cours
            try:
                reservation = Reservation.objects.get(
                    user=self.request.user, 
                    course=self.object
                )
                user_has_reservation = True
            except Reservation.DoesNotExist:
                user_has_reservation = False
        
        # Ajouter les informations au contexte
        context['user_has_reservation'] = user_has_reservation
        context['reservation'] = reservation
        context['available_spots'] = available_spots
        context['total_spots'] = total_spots
        context['reserved_spots'] = reserved_spots
        context['fill_percentage'] = fill_percentage
        context['is_full'] = available_spots <= 0
        
        return context
    
    @login_required
    def course_reservations(request, course_id):
        """Vue pour afficher toutes les réservations d'un cours (pour les coachs)"""
        course = get_object_or_404(Course, id=course_id)
        
        # Vérifier si l'utilisateur est le coach du cours ou un administrateur
        if not (request.user.is_superuser or (hasattr(request.user, 'coach') and request.user.coach == course.coach)):
            messages.error(request, "Vous n'avez pas la permission d'accéder à cette page.")
            return redirect('index')
        
        # Récupérer toutes les inscriptions actives pour ce cours
        enrollments = Enrollment.objects.filter(course=course, is_active=True).order_by('date_enrolled')
        
        return render(request, 'gym/course_reservations.html', {
            'course': course,
            'enrollments': enrollments
        })