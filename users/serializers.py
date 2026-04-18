from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'email', 'phone', 'role', 'is_staff', 'password')
        extra_kwargs = {
            'username': {'required': False},
        }

    def create(self, validated_data):
        if 'username' not in validated_data:
            validated_data['username'] = validated_data['email']
            
        request = self.context.get('request')
        
        # If no request (e.g. signal, management command) or user is not an admin, force STUDENT role
        is_admin = request and request.user and request.user.is_authenticated and request.user.role == 'ADMIN'
        
        if not is_admin:
            validated_data['role'] = 'STUDENT'
        elif 'role' not in validated_data:
            validated_data['role'] = 'STUDENT' # Default for admins if not specified
             
        return User.objects.create_user(**validated_data)

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name')
