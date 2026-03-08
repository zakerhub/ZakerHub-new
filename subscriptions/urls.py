from rest_framework.routers import DefaultRouter
from .views import SubscriptionOptionViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'options', SubscriptionOptionViewSet, basename='subscriptionoption')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = router.urls
