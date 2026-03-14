from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SubscriptionOption, Enrollment
from .serializers import SubscriptionOptionSerializer, EnrollmentSerializer
from datetime import date, timedelta
from django.utils import timezone

class IsRoleAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'ADMIN'

class SubscriptionOptionViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionOption.objects.all()
    serializer_class = SubscriptionOptionSerializer
    permission_classes = [IsAdminOrReadOnly]

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Enrollment.objects.all()
        if user.role == 'TEACHER':
            return Enrollment.objects.filter(subscription_option__course__teacher=user)
        if user.role == 'STUDENT':
            return Enrollment.objects.filter(student=user)
        return Enrollment.objects.none()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user, status='PENDING')

