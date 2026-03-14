from rest_framework import serializers
from .models import Curriculum, Subject, Course, Level, CourseItem
from users.serializers import PublicUserSerializer

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

class SubscriptionOptionMinimalSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='level.name', allow_null=True, read_only=True)
    level_id = serializers.IntegerField(source='level.id', allow_null=True, read_only=True)

    class Meta:
        from subscriptions.models import SubscriptionOption
        model = SubscriptionOption
        fields = ['id', 'plan_type', 'price', 'duration_days', 'level_id', 'level_name']

class StudentProgressSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import StudentProgress
        model = StudentProgress
        fields = ['is_completed', 'completed_at']

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
    subscription_options = SubscriptionOptionMinimalSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'subject', 'subject_name', 'teacher', 'teacher_name', 'description', 'subscription_options', 'created_at', 'updated_at')

class CourseDetailSerializer(CourseSerializer):
    teacher = PublicUserSerializer(read_only=True)
    # items = ... (only if enrolled)

class CourseItemSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = CourseItem
        fields = ('id', 'course', 'course_name', 'level', 'type', 'title', 'content_url', 'file', 'is_completed', 'created_at')

    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from .models import StudentProgress
            return StudentProgress.objects.filter(student=request.user, course_item=obj, is_completed=True).exists()
        return False
