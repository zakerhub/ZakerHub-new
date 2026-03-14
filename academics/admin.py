from django.contrib import admin
from .models import Curriculum, Subject, Course, Level, CourseItem

@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'curriculum', 'created_at')
    list_filter = ('curriculum',)
    search_fields = ('name',)

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'created_at')
    list_filter = ('subject', 'teacher')
    search_fields = ('subject__name', 'teacher__email')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'ADMIN':
            return qs
        return qs.filter(teacher=request.user)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not (request.user.is_superuser or request.user.role == 'ADMIN'):
            if 'teacher' in fields:
                fields.remove('teacher')
        return fields

    def save_model(self, request, obj, form, change):
        if not (request.user.is_superuser or request.user.role == 'ADMIN'):
            obj.teacher = request.user
        super().save_model(request, obj, form, change)

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(CourseItem)
class CourseItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'type', 'file', 'level', 'created_at')
    list_filter = ('course', 'type', 'level')
    search_fields = ('title',)

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
