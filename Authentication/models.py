from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils import timezone
import uuid
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from business.models import User
 
class OTPVerification(models.Model):
    OTP_FOR_CHOICES = [
        ('REGISTER', 'Register'),
        ('FORGOT_PASSWORD', 'Forgot Password'),
      
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    otp = models.CharField(max_length=6)  
    purpose = models.CharField(max_length=20, choices=OTP_FOR_CHOICES,default='REGISTER')
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)  

    def __str__(self):
        return f"OTP for {self.user.username}: {self.otp}"

    def is_expired(self):
         
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)

 