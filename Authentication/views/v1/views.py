
from cProfile import Profile
from Authentication.serializers import * 
from Authentication.models import *
from rest_framework import status
from django.contrib.auth import authenticate
import random
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.views import APIView
from rest_framework.response import Response
from Authentication.Constants.Email import send_email_to_user
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg


class VendorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendor_data = VendorSerializer(request.user).data
        return Response(vendor_data)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/"
    client_class = OAuth2Client

    def get_response(self):
        response = super().get_response()   
        #we can update the response here if needed
        return response
 
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Create OTP
            otp = random.randint(100000, 999999)
            OTPVerification.objects.create(user=user, otp=otp, purpose="REGISTER", created_at=timezone.now())

            # Send OTP Email
            context = {'otp': otp, 'username': user.username}
            print(otp)
            send_email_to_user(
                subject='Verify Your Email',
                context=context,
                template_path='otp_email_optimized.html',
                recipient_list=[user.email],
            )

            return Response({
                'status': 'Created',
                'user': {
                    'id': user.id,
                    'name': user.username,
                    'email': user.email,
                },
                'message': 'OTP sent to your email. Please verify your account.'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
class VerifyOTPView(APIView):
    def post(self, request):
        user_email = request.data.get('email')
        otp = request.data.get('otp_code')
        print(user_email, otp,"=====================================")

        try:
            otp_record = OTPVerification.objects.get(otp=otp)
            user = User.objects.get(email=otp_record.user.email)
        except OTPVerification.DoesNotExist:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        if timezone.now() > otp_record.created_at + timezone.timedelta(minutes=10):
            return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

        context = {
            "username": user.username,
        }

        if otp_record.purpose == 'REGISTER':
            user = otp_record.user
            user.is_active = True
            user.save()
            otp_record.delete()  # Delete only after we're done
            send_email_to_user(
                subject='Welcome To Evergreen',
                context=context,
                template_path='welcome-email.html',
                recipient_list=[user_email],
            )
        elif otp_record.purpose == 'FORGOT_PASSWORD':
            otp_record.is_used = True
            otp_record.save()

        return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)

 

class ResendOTPView(APIView):
    def post(self, request):
        user_email = request.data.get('email')
         

         
        if not user_email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=user_email).first()
        if not user:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        try: 
            OTPVerification.objects.filter(user=user).delete()

         
            otp = random.randint(100000, 999999)
            OTPVerification.objects.create(user=user, otp=otp, created_at=timezone.now())

            print(otp)
            context = {
                'otp': otp,
                'username': user.username,
            }
            
            send_email_to_user(
                subject='Verify Your Email',
                context=context,
                template_path='MarketPlace/otp_email_optimized.html',
                
                recipient_list=[user_email],
        )
             
         
           

            return Response({'message': 'A new OTP has been sent to your email.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'Server error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
             
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        
        user = authenticate(username=user.username, password=password)

        if user is not None:
             
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'Logged in',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
 
class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                otp = str(random.randint(100000, 999999))
                OTPVerification.objects.create(user=user, otp=otp,purpose="FORGOT_PASSWORD", created_at=timezone.now())

                print("otp",otp)
                context = {
                'otp': otp,
                'username': user.username,
                'email': email,
                }

                send_email_to_user(
                subject='Password Reset OTP',
                context=context,
                template_path='MarketPlace/password_reset_email.html',
                recipient_list=[email],
            )
                return Response({'message': 'OTP sent to your email'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']

            try:
                otp = OTPVerification.objects.filter(user__email=email, is_used=True).latest('created_at')
                if otp.is_expired():
                    return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)

                user = otp.user
                user.set_password(new_password)
                user.save()
                otp.delete()
                return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)

            except OTPVerification.DoesNotExist:
                return Response({'error': 'Invalid OTP or email'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
           
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class GetProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the profile of the currently logged-in user
        profile = request.user.profile  # Assuming there is a OneToOne relationship between User and Profile
        serializer = GetProfileSerializer(profile)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)


