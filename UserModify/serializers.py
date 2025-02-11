from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.utils.crypto import get_random_string
from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings


# Serializers of the undead , USERS


User = get_user_model()  


class UserVoidSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role']  

    # Validate that password and password2 match
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    # Create user, hash password, and remove password2
    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2, not needed in the DB
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', 'Academy'),  # Default role is academy
        )
        user.set_password(validated_data['password'])  # Hash password
        user.save()

        return user









class UserVoidLoginSerializer(serializers.Serializer):
    emailusername = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        # Extract and process email/username and password
        emailusername = data.get('emailusername', '').strip()
        password = data.get('password')

        user = None

        try:
            if '@' in emailusername:
                # Convert email to lowercase before querying
                emailusername = emailusername.lower()
                user = User.objects.get(email=emailusername)
            else:
                user = User.objects.get(username=emailusername)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email/username or password.")
        
        # Manually check the password
        if not check_password(password, user.password) or user is None:
            raise serializers.ValidationError("Invalid email/username or password.")

        # Everything checks out, return validated data along with the user
        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']
        
        # Generate refresh and access tokens for the authenticated user
        refresh = RefreshToken.for_user(user)
        refresh['email'] = user.email
        refresh['role'] = user.role

        access = refresh.access_token
        access['email'] = user.email
        access['role'] = user.role

        return {
            'refresh': str(refresh),
            'access': str(access),
            'user': {
                'email': user.email,
                'username': user.username,
                'role': user.role  
            }
        }







class UserVoidLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()  # Accepts the refresh token in the request

    def validate(self, attrs):
        # Validate that the 'refresh' field exists
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        # Try to blacklist the token
        try:
            token = RefreshToken(self.token)
            token.blacklist()  # Blacklists the token so it cannot be used again
        except Exception as e:
            self.fail('bad_token' , 'Token is invalid or expired.')  # If it fails, raise a bad token error.



