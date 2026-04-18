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
import time
import hashlib
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def staff_only(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(staff_only)
def vimeo_upload_page(request):
    return render(request, "vimeo_upload.html")

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (request.user.role == 'ADMIN')

class IsTeacherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

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

class VimeoUploadAPIView(APIView):
    permission_classes = [IsTeacherOrAdmin]

    def post(self, request):
        title = request.data.get("title", "").strip()
        size = request.data.get("size")
        
        if not title:
            return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not size:
            return Response({"error": "File size is required for Vimeo upload"}, status=status.HTTP_400_BAD_REQUEST)

        token = settings.VIMEO_ACCESS_TOKEN
        if not token:
            return Response({"error": "Missing VIMEO_ACCESS_TOKEN"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            r = requests.post(
                "https://api.vimeo.com/me/videos",
                headers={
                    "Authorization": f"bearer {token}",
                    "Content-Type": "application/json",
                    "Accept": "application/vnd.vimeo.*+json;version=3.4"
                },
                json={
                    "upload": {
                        "approach": "tus",
                        "size": size
                    },
                    "name": title
                },
                timeout=30,
            )
            r.raise_for_status()
            data = r.json()
            
            upload_link = data.get("upload", {}).get("upload_link")
            uri = data.get("uri")
            video_id = uri.split("/")[-1] if uri else None

            if not upload_link or not video_id:
                return Response({"error": "Failed to get upload link or video ID from Vimeo"}, status=status.HTTP_400_BAD_REQUEST)
                
        except requests.RequestException as e:
            return Response({"error": f"Vimeo API error: {e}"}, status=status.HTTP_502_BAD_GATEWAY)

        return Response({
            "uploadUrl": upload_link,
            "videoId": video_id,
            "embedUrl": f"https://player.vimeo.com/video/{video_id}",
        }, status=status.HTTP_201_CREATED)
