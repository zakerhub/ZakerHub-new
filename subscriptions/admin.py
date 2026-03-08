from django.contrib import admin
from .models import SubscriptionOption, Enrollment
from datetime import date, timedelta
from django.utils import timezone

@admin.register(SubscriptionOption)
class SubscriptionOptionAdmin(admin.ModelAdmin):
    list_display = ('course', 'level', 'plan_type', 'price', 'duration_days')
    list_filter = ('plan_type', 'course', 'level')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'subscription_option', 'status', 'start_date', 'end_date', 'approved_by')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('student__email', 'student__name', 'subscription_option__course__subject__name')
    actions = ['approve_enrollments', 'reject_enrollments']

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
