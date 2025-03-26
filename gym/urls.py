from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('enrollment/', views.enroll_course, name='enrollment'),
    
    # URLs pour le CRUD des entraîneurs
    path('coaches/', views.CoachListView.as_view(), name='coach-list'),
    path('coaches/<int:pk>/', views.CoachDetailView.as_view(), name='coach-detail'),
    path('coaches/new/', views.CoachCreateView.as_view(), name='coach-create'),
    path('coaches/<int:pk>/update/', views.CoachUpdateView.as_view(), name='coach-update'),
    path('coaches/<int:pk>/delete/', views.CoachDeleteView.as_view(), name='coach-delete'),
    
    # URLs pour le CRUD des cours
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('courses/new/', views.CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course-update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course-delete'),
]