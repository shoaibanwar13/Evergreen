
from Authentication.views.v1.views import *
from django.urls import path,include


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework.routers import DefaultRouter
 

 
urlpatterns = [
    path('vendor/', VendorAPIView.as_view(), name='vendor-api'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyOTPView.as_view(), name='verify-otp'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path("resend-otp/",ResendOTPView.as_view(),name="resend-otp"),
    path('get-user-profile/', GetProfileView.as_view(), name='get-profile'),
    path('edit-profile/', ProfileUpdateView.as_view(), name='profile-update'),
]
