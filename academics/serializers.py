from rest_framework import serializers
from .models import Curriculum, Subject, Course, Level, CourseItem
from users.serializers import PublicUserSerializer

class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

class CourseDetailSerializer(CourseSerializer):
    teacher = PublicUserSerializer(read_only=True)
    # items = ... (only if enrolled)

class CourseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseItem
        fields = '__all__'
