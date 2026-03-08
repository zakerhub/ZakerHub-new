from rest_framework import serializers
from .models import SubscriptionOption, Enrollment
from users.serializers import UserSerializer
from academics.serializers import CourseSerializer, LevelSerializer

class SubscriptionOptionSerializer(serializers.ModelSerializer):
    course_detail = CourseSerializer(source='course', read_only=True)
    level_detail = LevelSerializer(source='level', read_only=True)

    class Meta:
        model = SubscriptionOption
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    subscription_detail = SubscriptionOptionSerializer(source='subscription_option', read_only=True)
    student_detail = UserSerializer(source='student', read_only=True)

    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ('student', 'status', 'approved_by', 'approved_at', 'start_date', 'end_date')

    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        validated_data['status'] = 'PENDING'
        return super().create(validated_data)
