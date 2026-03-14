from django.db import models
from django.conf import settings

class Curriculum(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='subjects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.curriculum.code})"

class Course(models.Model):
    name = models.CharField(max_length=255, default="Unnamed Course")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses_taught')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject.name} - {self.teacher}"

class Level(models.Model):
    NAME_CHOICES = (
        ('BASIC', 'Basic'),
        ('ADVANCED', 'Advanced'),
    )
    name = models.CharField(max_length=20, choices=NAME_CHOICES, unique=True) 

    def __str__(self):
        return self.name

class CourseItem(models.Model):
    TYPE_CHOICES = (
        ('MATERIAL', 'Material'),
        ('ASSIGNMENT', 'Assignment'),
        ('MEETING', 'Meeting'),
        ('ANNOUNCEMENT', 'Announcement'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='items')
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    content_url = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='course_items/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

class StudentProgress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    course_item = models.ForeignKey(CourseItem, on_delete=models.CASCADE, related_name='progress')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course_item')
        verbose_name_plural = "Student Progress"

    def __str__(self):
        return f"{self.student.email} - {self.course_item.title} ({'Done' if self.is_completed else 'Pending'})"
