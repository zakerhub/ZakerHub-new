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

    def validate(self, data):
        student = self.context['request'].user
        option = data.get('subscription_option')
        
        if not option:
            raise serializers.ValidationError("Subscription option is required.")
            
        # Check if student already has a PENDING or APPROVED enrollment for the same COURSE and LEVEL
        existing = Enrollment.objects.filter(
            student=student, 
            subscription_option__course=option.course,
            subscription_option__level=option.level,
            status__in=['PENDING', 'APPROVED']
        ).exists()
        
        if existing:
            level_name = option.level.name if option.level else "this level"
            raise serializers.ValidationError(f"You already have an active or pending enrollment for {level_name}.")
            
        return data

    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        validated_data['status'] = 'PENDING'
        return super().create(validated_data)
