from rest_framework import serializers
from apps.accounts.models import User, UserProfile
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'is_active']
        read_only_fields = ['id', 'role', 'is_active']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar_url', 'location', 'phone_number', 'date_of_birth']

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add custom claims
        data['user'] = UserSerializer(self.user).data
        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirmation', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        try:
            password_validation.validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e)})
            
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data)
        return user
