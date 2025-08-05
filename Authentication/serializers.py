
from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from business.models import Profile
User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[validate_email])
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    phone_number = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'phone_number']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists.")
        return value

    def create(self, validated_data):
        username = validated_data['email'].split('@')[0]
        validated_data['username'] = username
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
 


# Serializer for Forgot Password
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

# Serializer for OTP Verification
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

# Serializer for Reset Password
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        from django.contrib.auth.password_validation import validate_password
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

class VendorSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(required=False)
    business_address = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email', 'company_name', 'business_address', 'first_name', 'last_name']

# Forgot Password View

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect")
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value
class GetProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    phone_number=serializers.CharField(source='user.phone_number', read_only=True)
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'country', 'profile_pic','phone_number']

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name','country', 'profile_pic']  # Add fields as needed

    def update(self, instance, validated_data):
        # Update the user fields first
        user_data = validated_data.pop('user', {})
        user = instance.user

        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()

        # Update the profile fields
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.country=validated_data.get('country', instance.country)
        instance.save()

        return instance

 
       