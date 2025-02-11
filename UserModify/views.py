from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from config import settings
from django.conf import settings
from .models import UserVoid
from .serializers import UserVoidSignupSerializer
from .serializers import UserVoidLoginSerializer
from rest_framework.views import APIView
from .serializers import UserVoidLogoutSerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from rest_framework import serializers
from drf_spectacular.utils import extend_schema


User = get_user_model()

# The Black Sun's views


class UserVoidSignupView(CreateAPIView):

    queryset = UserVoid.objects.all()
    serializer_class = UserVoidSignupSerializer
    permission_classes = [AllowAny]  # Anyone can sign up, no authentication required

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)  # Get the request data
        serializer.is_valid(raise_exception=True)  # Validate the data

        self.perform_create(serializer)  # Create the user (calls serializer's create method)
        headers = self.get_success_headers(serializer.data)  # Generate response headers

        return Response(
            {"message": "User created successfully", "user": serializer.data}, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )



class UserVoidLoginView(APIView):
    
    @extend_schema(
        request=UserVoidLoginSerializer,
        responses={200: UserVoidLoginSerializer}  
    )
    def post(self, request, *args, **kwargs):
        # Create a serializer instance with the incoming request data
        serializer = UserVoidLoginSerializer(data=request.data)

        # Validate the request data
        if serializer.is_valid():
            tokens = serializer.save()  # Get the tokens from the serializer
            
            access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

            # Set cookies for access and refresh tokens
            response = Response({
                "message": "Login successful",
                "user": tokens['user'],  # Return user info
                "access": tokens['access'],  # Include access token
                "refresh": tokens['refresh'],  # Include refresh token
            }, status=status.HTTP_200_OK)

            # Set access and refresh tokens in HTTP-only cookies
            response.set_cookie(
                key="access_token",
                value=tokens["access"],
                httponly=True,
                secure=True,
                max_age=int(access_token_lifetime.total_seconds()),
            )
            response.set_cookie(
                key="refresh_token",
                value=tokens["refresh"],
                httponly=True,
                secure=True,
                max_age=int(refresh_token_lifetime.total_seconds()),
            )
            return response
        
        # If invalid, return error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


 

class UserVoidLogoutView(APIView):
    @extend_schema(
        request=UserVoidLogoutSerializer,
        responses={204: None}  # Indicates no content in the response, but it was successful
    )
    def post(self, request):
        # Pass the refresh token to the LogoutSerializer
        serializer = UserVoidLogoutSerializer(data=request.data)
        
        # If the token is valid and successfully blacklisted, clear the cookies
        if serializer.is_valid():
            try:
                # Try to blacklist the refresh token
                token = RefreshToken(serializer.validated_data['refresh'])
                token.blacklist()  # Blacklist the token so it cannot be used again
            except InvalidToken:
                # If the token is invalid, handle it gracefully
                return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
            except TokenError as e:
                # Handle any other token related errors
                return Response({"detail": f"Token error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

            # Prepare a successful response
            response = Response({"detail": "Logout successful"}, status=status.HTTP_204_NO_CONTENT)
            
            # Clear cookies
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            
            return response
        
        # If the serializer is not valid, return a bad request error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




