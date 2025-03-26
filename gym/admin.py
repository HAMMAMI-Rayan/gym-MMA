from django.contrib import admin
from .models import Coach, Course, Member, Enrollment

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('user', 'speciality', 'experience')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'speciality')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'coach', 'level', 'max_students', 'schedule')
    list_filter = ('level', 'coach')
    search_fields = ('name', 'description', 'coach__user__username')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'phone')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')
    list_filter = ('date_of_birth',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('member', 'course', 'date_enrolled', 'is_active')
    list_filter = ('is_active', 'date_enrolled', 'course')
    search_fields = ('member__user__username', 'course__name')