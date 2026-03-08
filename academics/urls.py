from rest_framework.routers import DefaultRouter
from .views import CurriculumViewSet, SubjectViewSet, LevelViewSet, CourseViewSet, CourseItemViewSet

router = DefaultRouter()
router.register(r'curriculums', CurriculumViewSet, basename='curriculum')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'levels', LevelViewSet, basename='level')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'items', CourseItemViewSet, basename='courseitem')

urlpatterns = router.urls
