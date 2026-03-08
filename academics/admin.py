from django.contrib import admin
from .models import Curriculum, Subject, Course, Level, CourseItem

@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'curriculum', 'created_at')
    list_filter = ('curriculum',)
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'created_at')
    list_filter = ('subject', 'teacher')
    search_fields = ('subject__name', 'teacher__email')

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(CourseItem)
class CourseItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'type', 'level', 'created_at')
    list_filter = ('course', 'type', 'level')
    search_fields = ('title',)
