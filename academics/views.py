from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Curriculum, Subject, Course, Level, CourseItem
from .serializers import CurriculumSerializer, SubjectSerializer, CourseSerializer, LevelSerializer, CourseItemSerializer
from subscriptions.models import Enrollment
from datetime import date
from django.db.models import Q

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
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subject', 'teacher']

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [IsTeacherOrAdmin()]

    def perform_create(self, serializer):
        # Admin can specific teacher, Teacher is assigned themselves
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
            today = date.today()
            # Get approved enrollments that are active
            enrollments = Enrollment.objects.filter(
                student=user,
                status='APPROVED',
                start_date__lte=today,
                end_date__gte=today
            )
            
            if not enrollments.exists():
                return queryset.none()

            q_obj = Q()
            for enrollment in enrollments:
                sub = enrollment.subscription_option
                c_id = sub.course_id
                l_id = sub.level_id
                
                # If subscription has a specific level, allowing checking that level + generic items (null level)
                if l_id:
                    q_obj |= Q(course_id=c_id, level_id=l_id) | Q(course_id=c_id, level__isnull=True)
                else:
                    # If subscription has no level (generic course), allow items with no level
                    q_obj |= Q(course_id=c_id, level__isnull=True)
            
            return queryset.filter(q_obj)

        return queryset.none()
