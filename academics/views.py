from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Curriculum, Subject, Course, Level, CourseItem, StudentProgress
from .serializers import CurriculumSerializer, SubjectSerializer, CourseSerializer, LevelSerializer, CourseItemSerializer
from subscriptions.models import Enrollment
from datetime import date
from django.db.models import Q
from django.utils import timezone

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (request.user.role == 'ADMIN')

class IsTeacherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['TEACHER', 'ADMIN']

class CurriculumViewSet(viewsets.ModelViewSet):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer
    permission_classes = [IsAdminOrReadOnly]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['curriculum']

class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = [IsAdminOrReadOnly]

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subject', 'teacher']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Course.objects.all()
        if user.role == 'TEACHER':
            return Course.objects.filter(teacher=user)
        return Course.objects.all()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [IsTeacherOrAdmin()]

    def perform_create(self, serializer):
        # Admin can specify teacher, Teacher is assigned themselves
        if self.request.user.role == 'TEACHER':
            serializer.save(teacher=self.request.user)
        else:
            serializer.save()

class CourseItemViewSet(viewsets.ModelViewSet):
    serializer_class = CourseItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course', 'level', 'type']

    def get_queryset(self):
        user = self.request.user
        queryset = CourseItem.objects.all()

        if user.role == 'ADMIN':
            return queryset
        
        if user.role == 'TEACHER':
            return queryset.filter(course__teacher=user)

        if user.role == 'STUDENT':
            # Get approved enrollments
            enrollments = Enrollment.objects.filter(
                student=user,
                status='APPROVED'
            )
            
            if not enrollments.exists():
                return queryset.none()

            q_obj = Q()
            for enrollment in enrollments:
                sub = enrollment.subscription_option
                c_id = sub.course_id
                l_id = sub.level_id
                
                # Filter items for this course and (option's level OR generic items)
                item_filter = Q(course_id=c_id)
                if l_id:
                    item_filter &= (Q(level_id=l_id) | Q(level__isnull=True))
                else:
                    item_filter &= Q(level__isnull=True)
                
                q_obj |= item_filter
            
            return queryset.filter(q_obj).distinct()

        return queryset.none()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def toggle_complete(self, request, pk=None):
        item = self.get_object()
        user = request.user
        
        progress, created = StudentProgress.objects.get_or_create(
            student=user,
            course_item=item
        )
        
        # If it was completed, uncomplete it. If not, complete it.
        progress.is_completed = not progress.is_completed
        if progress.is_completed:
            progress.completed_at = timezone.now()
        else:
            progress.completed_at = None
            
        progress.save()
        
        return Response({
            'status': 'success',
            'is_completed': progress.is_completed,
            'completed_at': progress.completed_at
        })
