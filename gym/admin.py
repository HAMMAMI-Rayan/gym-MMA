from django.contrib import admin
from .models import UserProfile, Course, Reservation

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_coach', 'phone_number')
    list_filter = ('is_coach',)
    search_fields = ('user__username', 'user__email', 'phone_number')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_type', 'level', 'coach', 'date', 'start_time', 'end_time', 'max_participants')
    list_filter = ('course_type', 'level', 'date', 'coach')
    search_fields = ('title', 'description', 'coach__username')
    date_hierarchy = 'date'

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at')
    list_filter = ('course__course_type', 'course__date')
    search_fields = ('user__username', 'course__title')
    date_hierarchy = 'created_at'