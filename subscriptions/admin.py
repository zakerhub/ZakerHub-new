from django.contrib import admin
from .models import SubscriptionOption, Enrollment
from academics.models import Course
from users.models import User
from datetime import date, timedelta
from django.utils import timezone

@admin.register(SubscriptionOption)
class SubscriptionOptionAdmin(admin.ModelAdmin):
    list_display = ('course', 'level', 'plan_type', 'price', 'duration_days')
    list_filter = ('plan_type', 'course', 'level')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'ADMIN':
            return qs
        return qs.filter(course__teacher=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            if not (request.user.is_superuser or request.user.role == 'ADMIN'):
                kwargs["queryset"] = Course.objects.filter(teacher=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'subscription_option', 'status', 'start_date', 'end_date', 'approved_by')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('student__email', 'student__name', 'subscription_option__course__subject__name')
    actions = ['approve_enrollments', 'reject_enrollments']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'ADMIN':
            return qs
        return qs.filter(subscription_option__course__teacher=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subscription_option":
            if not (request.user.is_superuser or request.user.role == 'ADMIN'):
                kwargs["queryset"] = SubscriptionOption.objects.filter(course__teacher=request.user)
        if db_field.name == "approved_by":
            if not (request.user.is_superuser or request.user.role == 'ADMIN'):
                kwargs["queryset"] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not (request.user.is_superuser or request.user.role == 'ADMIN'):
            # Teachers shouldn't set who approved it manually, it's auto-set in action
            if 'approved_by' in fields:
                fields.remove('approved_by')
        return fields

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        # Admins can delete, teachers can't delete enrollments (optional safety)
        return request.user.is_superuser or request.user.role == 'ADMIN'

    def approve_enrollments(self, request, queryset):
        for enrollment in queryset:
            if enrollment.status != 'APPROVED':
                enrollment.status = 'APPROVED'
                enrollment.approved_by = request.user
                enrollment.approved_at = timezone.now()
                
                # Calculate dates
                duration = enrollment.subscription_option.duration_days
                enrollment.start_date = date.today()
                enrollment.end_date = date.today() + timedelta(days=duration)
                enrollment.save()
    
    approve_enrollments.short_description = "Approve selected enrollments (Calculates Dates)"

    def reject_enrollments(self, request, queryset):
        queryset.update(status='REJECTED')
    
    reject_enrollments.short_description = "Reject selected enrollments"
