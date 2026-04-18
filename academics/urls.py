from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurriculumViewSet, SubjectViewSet, LevelViewSet, CourseViewSet, CourseItemViewSet, VimeoUploadAPIView

router = DefaultRouter()
router.register(r'curriculums', CurriculumViewSet, basename='curriculum')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'levels', LevelViewSet, basename='level')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'items', CourseItemViewSet, basename='courseitem')

urlpatterns = [
    path('', include(router.urls)),
    path('vimeo/upload/', VimeoUploadAPIView.as_view(), name='vimeo-upload'),
]
