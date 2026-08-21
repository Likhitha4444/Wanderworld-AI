from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from apps.accounts.serializers import RegisterSerializer, UserSerializer, LoginSerializer, UserProfileSerializer
from django.contrib.auth import update_session_auth_hash, get_user_model
from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail

User = get_user_model()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ADMIN')

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "success": True,
                "message": "Registration successful.",
                "data": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "success": False,
            "message": "Registration failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "success": True,
                "message": "Login successful.",
                "data": serializer.validated_data
            }, status=status.HTTP_200_OK)
        return Response({
            "success": False,
            "message": "Invalid credentials.",
            "errors": serializer.errors
        }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception:
            return Response({
                "success": False,
                "message": "Logout failed."
            }, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        new_password_confirmation = request.data.get('new_password_confirmation')

        if not current_password or not new_password or not new_password_confirmation:
            return Response({"success": False, "message": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != new_password_confirmation:
            return Response({"success": False, "message": "New passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.check_password(current_password):
            return Response({"success": False, "message": "Incorrect current password."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        
        return Response({"success": True, "message": "Password changed successfully."})

import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# ...

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"success": False, "message": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_url = f"http://localhost:3000/reset-password/{uid}/{token}/"
            
            subject = 'Reset your WanderWorld password'
            email_body = (
                "Hello,\n\n"
                "We received a request to reset your WanderWorld password.\n\n"
                "Click the link below to create a new password:\n"
                f"{reset_url}\n\n"
                "If you did not request this, you can safely ignore this email.\n\n"
                "Regards,\n"
                "WanderWorld Team"
            )
            
            try:
                send_mail(
                    subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(f"SMTP Email sending failed: {str(e)}")
                return Response({"success": False, "message": f"Email could not be sent: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"success": True, "message": "If an account with that email exists, you will receive a password reset link."})

class ResetPasswordView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"success": False, "message": "Invalid link."}, status=status.HTTP_400_BAD_REQUEST)
        
        if default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            new_password_confirmation = request.data.get('new_password_confirmation')
            
            if not new_password or not new_password_confirmation:
                return Response({"success": False, "message": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
            
            if new_password != new_password_confirmation:
                return Response({"success": False, "message": "New passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)
            user.save()
            return Response({"success": True, "message": "Password reset successfully."})
        
        return Response({"success": False, "message": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            "success": True,
            "message": "User details retrieved successfully.",
            "data": serializer.data
        })

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user.profile)
        return Response({
            "success": True,
            "message": "Profile retrieved successfully.",
            "data": serializer.data
        })

    def patch(self, request):
        serializer = UserProfileSerializer(request.user.profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Profile updated successfully.",
                "data": serializer.data
            })
        return Response({
            "success": False,
            "message": "Profile update failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
