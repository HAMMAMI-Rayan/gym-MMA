from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    
    
    path('logout/', views.logout_view, name='logout'),  # Vue de déconnexion personnalisée
    
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/new/', views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    
    path('courses/<int:course_id>/reserve/', views.reserve_course, name='reserve_course'),
    path('reservations/<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    
    path('coach/dashboard/', views.CoachDashboardView.as_view(), name='coach_dashboard'),
    path('courses/<int:course_id>/reserve/', views.reserve_course, name='reserve-course'),
    path('reservation/<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel-reservation'),
]